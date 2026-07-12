from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import PlainTextResponse
from collections import deque
import redis
from fastapi import Header, HTTPException
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
import base64
from collections import defaultdict, deque
from fastapi import Response
import jwt
import json
import numpy as np
import yaml
import os
import time
import uuid
import requests
from dotenv import dotenv_values
from pathlib import Path

app = FastAPI()

# -------------------- CORS --------------------
# ALLOWED_ORIGIN = ["https://dash-jofexd.example.com","https://exam.sanand.workers.dev"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# -------------------- Custom Headers --------------------
class HeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        # ---------------- Rate Limiting ----------------
        client = request.headers.get("X-Client-Id")

        if client and request.url.path.startswith("/orders"):
        
            key = f"rate:{client}"
        
            current = redis_client.incr(key)
        
            if current == 1:
                redis_client.expire(key, WINDOW_SECONDS)
        
            if current > RATE_LIMIT:
                ttl = redis_client.ttl(key)
        
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"},
                    headers={
                        "Retry-After": str(max(ttl, 1))
                    },
                )        # ---------------- Metrics ----------------
        REQUEST_COUNTER.inc()

        # ---------------- Request ID ----------------
        request_id = str(uuid.uuid4())

        response = await call_next(request)

        process_time = time.perf_counter() - start

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        # ---------------- Structured Logs ----------------
        LOGS.append({
            "level": "INFO",
            "ts": time.time(),
            "path": request.url.path,
            "request_id": request_id,
        })

        return response


app.add_middleware(HeaderMiddleware)

# -------------------- Load Latency Data --------------------
DATA_FILE = Path(__file__).resolve().parent.parent / "q-vercel-latency.json"

with open(DATA_FILE) as f:
    DATA = json.load(f)

# -------------------- JWT Verification Config --------------------
ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-5f3lu8ub.apps.exam.local"

PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuY
cxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfW
ed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfI
SI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----
"""
API_KEY = "ak_fjkk4xvbqfsfey6x07qpw5xy"

START_TIME = time.time()

REQUEST_COUNTER = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

LOGS = deque(maxlen=1000)
# -------------------- Orders Assignment --------------------

TOTAL_ORDERS = 54
RATE_LIMIT = 17
WINDOW_SECONDS = 10

IDEMPOTENCY_STORE = {}

import redis
import os

redis_client = redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True,
)

NEXT_ORDER_ID = 1

def encode_cursor(index: int) -> str:
    return base64.b64encode(str(index).encode()).decode()


def decode_cursor(cursor: str) -> int:
    try:
        return int(base64.b64decode(cursor.encode()).decode())
    except Exception:
        return 0




class TokenRequest(BaseModel):
    token: str
class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: list[Event]
# -------------------- Health Endpoint --------------------
@app.get("/")
async def health():
    return {"status": "ok"}

# -------------------- Latency Assignment --------------------
@app.post("/")
async def metrics(payload: dict):
    regions = payload["regions"]
    threshold = payload["threshold_ms"]

    result = {}

    for region in regions:
        rows = [r for r in DATA if r["region"] == region]

        latencies = [r["latency_ms"] for r in rows]
        uptimes = [r["uptime_pct"] for r in rows]

        result[region] = {
            "avg_latency": sum(latencies) / len(latencies),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": sum(uptimes) / len(uptimes),
            "breaches": sum(1 for x in latencies if x > threshold),
        }

    return {"regions": result}

# -------------------- Stats Assignment --------------------
@app.get("/stats")
async def stats(values: str = Query(...)):
    nums = [int(x.strip()) for x in values.split(",") if x.strip()]

    return {
        "email": "23f3004142@ds.study.iitm.ac.in",
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }

# -------------------- OAuth/JWT Verification --------------------
@app.post("/verify")
async def verify(data: TokenRequest):
    try:
        payload = jwt.decode(
            data.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
        )

        return {
            "valid": True,
            "email": payload.get("email"),
            "sub": payload.get("sub"),
            "aud": payload.get("aud"),
        }

    except jwt.PyJWTError:
        return JSONResponse(
            status_code=401,
            content={"valid": False},
        )
# -------------------- 12-Factor Config Assignment --------------------

DEFAULT_CONFIG = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.development.yaml"
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def parse_bool(value):
    return str(value).strip().lower() in (
        "true",
        "1",
        "yes",
        "on",
    )


def coerce(key, value):
    if key in ("port", "workers"):
        return int(value)

    if key == "debug":
        return parse_bool(value)

    return str(value)


@app.get("/effective-config")
async def effective_config(set: list[str] = Query(default=[])):
    # Layer 1 : Defaults
    config = DEFAULT_CONFIG.copy()

    # Layer 2 : config.development.yaml
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            yaml_config = yaml.safe_load(f) or {}

        for key, value in yaml_config.items():
            config[key] = coerce(key, value)

    # Layer 3 : .env
    if ENV_FILE.exists():
        env_config = dotenv_values(ENV_FILE)

        # Alias NUM_WORKERS -> workers
        if "NUM_WORKERS" in env_config:
            env_config["workers"] = env_config.pop("NUM_WORKERS")

        for key, value in env_config.items():
            if value is not None:
                config[key] = coerce(key, value)

    # Layer 4 : APP_* OS Environment Variables
    env_mapping = {
        "APP_PORT": "port",
        "APP_WORKERS": "workers",
        "APP_DEBUG": "debug",
        "APP_LOG_LEVEL": "log_level",
        "APP_API_KEY": "api_key",
    }

    for env_key, config_key in env_mapping.items():
        value = os.getenv(env_key)

        if value is not None:
            config[config_key] = coerce(config_key, value)

    # Layer 5 : CLI overrides (?set=key=value)
    for item in set:
        if "=" not in item:
            continue

        key, value = item.split("=", 1)
        config[key] = coerce(key, value)

    # Secret masking
    config["api_key"] = "****"

    return {
        "port": config["port"],
        "workers": config["workers"],
        "debug": config["debug"],
        "log_level": config["log_level"],
        "api_key": config["api_key"],
    }
@app.post("/analytics")
async def analytics(
    data: AnalyticsRequest,
    x_api_key: str = Header(None)
):
    # Authentication
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    events = data.events

    total_events = len(events)

    unique_users = len(set(event.user for event in events))

    revenue = sum(
        event.amount
        for event in events
        if event.amount > 0
    )

    totals = {}

    for event in events:
        if event.amount > 0:
            totals[event.user] = totals.get(event.user, 0) + event.amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": "23f3004142@ds.study.iitm.ac.in",
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }
@app.get("/work")
async def work(n: int = Query(...)):
    for _ in range(n):
        pass

    return {
        "email": "23f3004142@ds.study.iitm.ac.in",
        "done": n,
    }
@app.get("/metrics")
async def metrics_prometheus():
    return PlainTextResponse(
        generate_latest().decode(),
        media_type=CONTENT_TYPE_LATEST,
    )
@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "uptime_s": time.time() - START_TIME,
    }
@app.get("/logs/tail")
async def logs(limit: int = Query(10)):
    return list(LOGS)[-limit:]

from typing import Optional
from fastapi import Header

@app.post("/orders")
async def create_order(
    request: Request,
    response: Response,
):
    global NEXT_ORDER_ID

    key = request.headers.get("Idempotency-Key")

    if not key:
        raise HTTPException(
            status_code=400,
            detail="Missing Idempotency-Key"
        )

    if key in IDEMPOTENCY_STORE:
        response.status_code = 200
        return IDEMPOTENCY_STORE[key]

    order = {
        "id": NEXT_ORDER_ID
    }

    NEXT_ORDER_ID += 1

    IDEMPOTENCY_STORE[key] = order

    response.status_code = 201
    return order
from typing import Optional
from fastapi import Header

@app.get("/orders")
async def list_orders(
    limit: int = Query(10),
    cursor: Optional[str] = None,
    x_client_id: Optional[str] = Header(None, alias="X-Client-Id"),
):
    start = 0

    if cursor:
        start = decode_cursor(cursor)

    end = min(start + limit, TOTAL_ORDERS)

    items = [
        {"id": i}
        for i in range(start + 1, end + 1)
    ]

    next_cursor = None

    if end < TOTAL_ORDERS:
        next_cursor = encode_cursor(end)

    return {
        "items": items,
        "next_cursor": next_cursor,
    }

class ProblemRequest(BaseModel):
    problem_id: str
    problem: str


@app.post("/solve")
async def solve(req: ProblemRequest):
    prompt = f"""
You are solving an arithmetic word problem.

Rules:
- Ignore irrelevant numbers.
- Compute the final integer answer.
- Return ONLY valid JSON.
- JSON must contain exactly two keys:
  {{
    "reasoning": "at least 80 characters",
    "answer": 123
  }}
- answer must be an integer.

Problem:
{req.problem}
"""

    response = requests.post(
        "https://aipipe.org/openrouter/v1/responses",
        headers={
            "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDQxNDJAZHMuc3R1ZHkuaWl0bS5hYy5pbiIsImlhdCI6MTc4MzcwMzQ0NiwiaXNzIjoiaHR0cHM6Ly9haXBpcGUub3JnIiwiYXVkIjoiYWlwaXBlLWFwaSIsImV4cCI6MTc4NDMwODI0Nn0.pNN9YGbM-wBzNS4WXKZS9VUjofm73nkABZ4vilCwf9U",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4.1-nano",
            "input": prompt,
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    data = response.json()
    print(response.json())
    # Responses API output
    text = data["output"][0]["content"][0]["text"]

    import json
    try:
        result = json.loads(text)
    except Exception:
        raise HTTPException(status_code=500, detail="Model returned invalid JSON")

    if set(result.keys()) != {"reasoning", "answer"}:
        raise HTTPException(status_code=500, detail="Invalid JSON keys")

    if not isinstance(result["reasoning"], str) or len(result["reasoning"]) < 80:
        raise HTTPException(status_code=500, detail="Invalid reasoning")

    if not isinstance(result["answer"], int):
        raise HTTPException(status_code=500, detail="Answer must be an integer")

    return result
class RankingRequest(BaseModel):
    query_id: str
    query: str
    candidates: list[str]

@app.post("/rank")
async def rank(req: RankingRequest):
    print("Reached endpoint")
    print(req.query)
    response = requests.post(
        "https://aipipe.org/openai/v1/embeddings",
        headers={
            "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDQxNDJAZHMuc3R1ZHkuaWl0bS5hYy5pbiIsImlhdCI6MTc4MzcwMzQ0NiwiaXNzIjoiaHR0cHM6Ly9haXBpcGUub3JnIiwiYXVkIjoiYWlwaXBlLWFwaSIsImV4cCI6MTc4NDMwODI0Nn0.pNN9YGbM-wBzNS4WXKZS9VUjofm73nkABZ4vilCwf9U",
            "Content-Type": "application/json",
        },
        json={
            "model": "text-embedding-3-small",
            "input": [req.query] + req.candidates
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=response.text
        )

    data = response.json()["data"]

    embeddings = [item["embedding"] for item in data]

    query_embedding = np.array(embeddings[0])

    scores = []

    for emb in embeddings[1:]:
        emb = np.array(emb)
        score = np.dot(query_embedding, emb) / (
            np.linalg.norm(query_embedding) *
            np.linalg.norm(emb)
        )
        scores.append(float(score))

    ranking = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:3]

    return {"ranking": ranking}
class InvoiceRequest(BaseModel):
    document_id: str
    text: str
    json_schema: dict = Field(alias="schema")

    model_config = {
        "populate_by_name": True
    }


@app.post("/extract")
async def extract(req: InvoiceRequest):

    prompt = (
        "Extract the invoice exactly according to the supplied JSON Schema. "
        "Return ONLY valid JSON."
    )

    response = requests.post(
        "https://aipipe.org/openrouter/v1/responses",
        headers={
            "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDQxNDJAZHMuc3R1ZHkuaWl0bS5hYy5pbiIsImlhdCI6MTc4MzcwMzQ0NiwiaXNzIjoiaHR0cHM6Ly9haXBpcGUub3JnIiwiYXVkIjoiYWlwaXBlLWFwaSIsImV4cCI6MTc4NDMwODI0Nn0.pNN9YGbM-wBzNS4WXKZS9VUjofm73nkABZ4vilCwf9U",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4.1-mini",
            "input": [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": req.text
                }
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "invoice",
                    "schema": req.json_schema
                }
            }
        },
        timeout=30,
    )
    # print(response.status_code)
    # print(response.text)
    # return response.json()
    if response.status_code != 200:
        raise HTTPException(500, response.text)

    data = response.json()

    import json

    return json.loads(
        response.json()["output"][0]["content"][0]["text"]
    )
class AudioRequest(BaseModel):
    audio_id: str
    audio_base64: str


@app.post("/analyze")
async def analyze(req: AudioRequest):

    response = requests.post(
        "https://aipipe.org/openrouter/v1/responses",
        headers={
            "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDQxNDJAZHMuc3R1ZHkuaWl0bS5hYy5pbiIsImlhdCI6MTc4MzcwMzQ0NiwiaXNzIjoiaHR0cHM6Ly9haXBpcGUub3JnIiwiYXVkIjoiYWlwaXBlLWFwaSIsImV4cCI6MTc4NDMwODI0Nn0.pNN9YGbM-wBzNS4WXKZS9VUjofm73nkABZ4vilCwf9U",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4.1-mini",
            "input": [
                {
                    "role": "system",
                    "content": (
                        "Analyze the supplied audio. "
                        "Return ONLY valid JSON matching exactly the required schema."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Extract the dataset represented in this audio and compute all requested statistics."
                        },
                        {
                            "type": "input_audio",
                            "audio": req.audio_base64,
                            "format": "wav"
                        }
                    ]
                }
            ]
        },
        timeout=60,
    )

    if response.status_code != 200:
        raise HTTPException(500, response.text)

    data = response.json()

    return json.loads(
        data["output"][0]["content"][0]["text"]
    )
class DynamicRequest(BaseModel):
    text: str
    input_schema: dict = Field(..., alias="schema")

    class Config:
        allow_population_by_field_name = True


@app.post("/dynamic-extract")
async def dynamic_extract(req: DynamicRequest):

    print("1. Reached endpoint")

    try:
        print("2. Schema =", req.input_schema)

        properties = {}
        required = []

        for field, field_type in req.input_schema.items():
            print("3.", field, field_type)

            properties[field] = {
                "type": "string"
            }

            required.append(field)

        print("4. JSON schema built")
        print("5. Before requests.post")

        response = requests.post(
            "https://httpbin.org/post",
            json={"hello": "world"},
            timeout=10,
        )

        print("6. Status:", response.status_code)

        return response.json()

    except Exception:
        import traceback
        traceback.print_exc()
        raise
