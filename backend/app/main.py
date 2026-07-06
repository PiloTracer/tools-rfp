"""RFP Platform — FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="RFP Platform API",
    description="Self-hosted RFP parsing, analysis, and draft generation platform",
    version="0.1.0",
)


@app.get("/health/live")
async def health_live():
    return {"status": "alive"}


@app.get("/health/ready")
async def health_ready():
    return {"status": "ready"}
