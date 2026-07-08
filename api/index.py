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
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import json
import numpy as np
import time
import uuid
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

# -------------------- Existing Health Endpoint --------------------
@app.get("/")
async def health():
    return {"status": "ok"}

# -------------------- Existing Latency Assignment --------------------
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

# -------------------- New Stats Assignment --------------------
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
