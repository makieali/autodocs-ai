"""Document generation endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from autodocs_ai.api.models import GenerateDocumentRequest, GenerateDocumentResponse
from autodocs_ai.core.generator import GenerateRequest, generate_document

router = APIRouter()


@router.post("/generate", response_model=list[GenerateDocumentResponse])
async def generate(request: GenerateDocumentRequest) -> list[GenerateDocumentResponse]:
    """Generate a document from a prompt."""
    gen_request = GenerateRequest(
        prompt=request.prompt,
        template=request.template,
        output_format=request.output_format,
        language=request.language,
        renderer=request.renderer,
        provider=request.provider,
    )

    try:
        responses = await generate_document(gen_request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    results = []
    for r in responses:
        results.append(
            GenerateDocumentResponse(
                output_path=str(r.output_path),
                output_format=r.output_format,
                model=r.ai_result.model,
                provider=r.ai_result.provider,
                usage=r.ai_result.usage,
            )
        )
    return results


@router.post("/generate/download")
async def generate_and_download(request: GenerateDocumentRequest) -> FileResponse:
    """Generate a document and return it as a file download."""
    gen_request = GenerateRequest(
        prompt=request.prompt,
        template=request.template,
        output_format=request.output_format,
        language=request.language,
        renderer=request.renderer,
        provider=request.provider,
    )

    try:
        responses = await generate_document(gen_request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not responses:
        raise HTTPException(status_code=500, detail="No output generated")

    response = responses[0]
    media_types = {
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "html": "text/html",
        "markdown": "text/markdown",
    }

    return FileResponse(
        path=str(response.output_path),
        media_type=media_types.get(response.output_format, "application/octet-stream"),
        filename=response.output_path.name,
    )
