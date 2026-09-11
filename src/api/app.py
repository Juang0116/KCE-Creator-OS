from fastapi import FastAPI

from .discovery import router as discovery_router


app = FastAPI(
    title="KCE Creator OS API",
    version="0.1.0",
)


app.include_router(discovery_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
    }