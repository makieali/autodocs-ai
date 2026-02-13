"""FastAPI application."""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

from autodocs_ai import __version__
from autodocs_ai.api.routes import documents, health
from autodocs_ai.config import get_settings

app = FastAPI(
    title="autodocs-ai",
    description="AI-powered document generator API. "
    "Generate professional PDF/DOCX/HTML documents from prompts.",
    version=__version__,
)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str | None = Security(api_key_header)) -> str | None:
    """Verify API key if one is configured."""
    settings = get_settings()
    if settings.api_key:
        if not api_key or api_key != settings.api_key:
            raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return api_key


# Include routes
app.include_router(health.router, tags=["health"])
app.include_router(
    documents.router,
    tags=["documents"],
    dependencies=[Depends(verify_api_key)],
)
