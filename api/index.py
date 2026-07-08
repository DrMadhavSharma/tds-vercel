# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import json
# import numpy as np

# app = FastAPI()

# app.add_middleware(
# CORSMiddleware,
# allow_origins=["*"],
# allow_methods=["POST", "GET", "OPTIONS"],
# allow_headers=["Content-Type", "Authorization"],
# expose_headers=["Access-Control-Allow-Origin"],
# )

# from pathlib import Path

# DATA_FILE = Path(__file__).resolve().parent.parent / "q-vercel-latency.json"

# with open(DATA_FILE) as f:
#     DATA = json.load(f)
    
# @app.get("/")
# async def health():
#     return {"status": "ok"}
# @app.post("/")
# async def metrics(payload: dict):
#     regions = payload["regions"]
#     threshold = payload["threshold_ms"]

#     result = {}

#     for region in regions:
#         rows = [r for r in DATA if r["region"] == region]

#         latencies = [r["latency_ms"] for r in rows]
#         uptimes = [r["uptime_pct"] for r in rows]

#         result[region] = {
#             "avg_latency": sum(latencies) / len(latencies),
#             "p95_latency": float(np.percentile(latencies, 95)),
#             "avg_uptime": sum(uptimes) / len(uptimes),
#             "breaches": sum(1 for x in latencies if x > threshold)
#         }

#     return {
#     "regions": result }
# from fastapi import FastAPI, Query, Request
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.base import BaseHTTPMiddleware
# import json
# import numpy as np
# import time
# import uuid
# from pathlib import Path

# app = FastAPI()

# # -------------------- CORS --------------------
# ALLOWED_ORIGIN = "https://dash-jofexd.example.com"

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[ALLOWED_ORIGIN],
#     allow_methods=["GET", "POST", "OPTIONS"],
#     allow_headers=["*"],
# )

# # -------------------- Custom Headers --------------------
# class HeaderMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         start = time.perf_counter()

#         response = await call_next(request)

#         process_time = time.perf_counter() - start

#         response.headers["X-Request-ID"] = str(uuid.uuid4())
#         response.headers["X-Process-Time"] = f"{process_time:.6f}"

#         return response

# app.add_middleware(HeaderMiddleware)

# # -------------------- Load Latency Data --------------------
# DATA_FILE = Path(__file__).resolve().parent.parent / "q-vercel-latency.json"

# with open(DATA_FILE) as f:
#     DATA = json.load(f)

# # -------------------- Existing Health Endpoint --------------------
# @app.get("/")
# async def health():
#     return {"status": "ok"}

# # -------------------- Existing Latency Assignment --------------------
# @app.post("/")
# async def metrics(payload: dict):
#     regions = payload["regions"]
#     threshold = payload["threshold_ms"]

#     result = {}

#     for region in regions:
#         rows = [r for r in DATA if r["region"] == region]

#         latencies = [r["latency_ms"] for r in rows]
#         uptimes = [r["uptime_pct"] for r in rows]

#         result[region] = {
#             "avg_latency": sum(latencies) / len(latencies),
#             "p95_latency": float(np.percentile(latencies, 95)),
#             "avg_uptime": sum(uptimes) / len(uptimes),
#             "breaches": sum(1 for x in latencies if x > threshold),
#         }

#     return {"regions": result}

# # -------------------- New Stats Assignment --------------------
# @app.get("/stats")
# async def stats(values: str = Query(...)):
#     nums = [int(x.strip()) for x in values.split(",") if x.strip()]

#     return {
#         "email": "23f3004142@ds.study.iitm.ac.in",
#         "count": len(nums),
#         "sum": sum(nums),
#         "min": min(nums),
#         "max": max(nums),
#         "mean": sum(nums) / len(nums),
#     }
# from fastapi import FastAPI, Query, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from starlette.middleware.base import BaseHTTPMiddleware
# from pydantic import BaseModel
# import jwt
# import json
# import numpy as np
# import time
# import uuid
# from pathlib import Path

# app = FastAPI()

# # -------------------- CORS --------------------
# ALLOWED_ORIGIN = "https://dash-jofexd.example.com"

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[ALLOWED_ORIGIN],
#     allow_methods=["GET", "POST", "OPTIONS"],
#     allow_headers=["*"],
# )

# # -------------------- Custom Headers --------------------
# class HeaderMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         start = time.perf_counter()

#         response = await call_next(request)

#         process_time = time.perf_counter() - start

#         response.headers["X-Request-ID"] = str(uuid.uuid4())
#         response.headers["X-Process-Time"] = f"{process_time:.6f}"

#         return response

# app.add_middleware(HeaderMiddleware)

# # -------------------- Load Latency Data --------------------
# DATA_FILE = Path(__file__).resolve().parent.parent / "q-vercel-latency.json"

# with open(DATA_FILE) as f:
#     DATA = json.load(f)

# # -------------------- JWT Verification Config --------------------
# ISSUER = "https://idp.exam.local"
# AUDIENCE = "tds-5f3lu8ub.apps.exam.local"

# PUBLIC_KEY = """
# -----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuY
# cxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMID
# EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXc
# WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfW
# ed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfI
# SI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIX
# dQIDAQAB
# -----END PUBLIC KEY-----
# """

# class TokenRequest(BaseModel):
#     token: str

# # -------------------- Existing Health Endpoint --------------------
# @app.get("/")
# async def health():
#     return {"status": "ok"}

# # -------------------- Existing Latency Assignment --------------------
# @app.post("/")
# async def metrics(payload: dict):
#     regions = payload["regions"]
#     threshold = payload["threshold_ms"]

#     result = {}

#     for region in regions:
#         rows = [r for r in DATA if r["region"] == region]

#         latencies = [r["latency_ms"] for r in rows]
#         uptimes = [r["uptime_pct"] for r in rows]

#         result[region] = {
#             "avg_latency": sum(latencies) / len(latencies),
#             "p95_latency": float(np.percentile(latencies, 95)),
#             "avg_uptime": sum(uptimes) / len(uptimes),
#             "breaches": sum(1 for x in latencies if x > threshold),
#         }

#     return {"regions": result}

# # -------------------- Existing Stats Assignment --------------------
# @app.get("/stats")
# async def stats(values: str = Query(...)):
#     nums = [int(x.strip()) for x in values.split(",") if x.strip()]

#     return {
#         "email": "23f3004142@ds.study.iitm.ac.in",
#         "count": len(nums),
#         "sum": sum(nums),
#         "min": min(nums),
#         "max": max(nums),
#         "mean": sum(nums) / len(nums),
#     }

# # -------------------- OAuth/JWT Verification Assignment --------------------
# @app.post("/verify")
# async def verify(data: TokenRequest):
#     try:
#         payload = jwt.decode(
#             data.token,
#             PUBLIC_KEY,
#             algorithms=["RS256"],
#             issuer=ISSUER,
#             audience=AUDIENCE,
#         )

#         return {
#             "valid": True,
#             "email": payload.get("email"),
#             "sub": payload.get("sub"),
#             "aud": payload.get("aud"),
#         }

#     except jwt.PyJWTError:
#         return JSONResponse(
#             status_code=401,
#             content={"valid": False},
#         )
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel

import jwt
import json
import numpy as np
import yaml
import os
import time
import uuid

from dotenv import dotenv_values
from pathlib import Path

app = FastAPI()

# -------------------- CORS --------------------
ALLOWED_ORIGIN = "https://dash-jofexd.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# -------------------- Custom Headers --------------------
class HeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start

        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{process_time:.6f}"

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

class TokenRequest(BaseModel):
    token: str

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
