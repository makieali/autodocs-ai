"""Document generation orchestrator."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from autodocs_ai.config import OutputFormat, RendererName, Settings, TemplateName, get_settings
from autodocs_ai.core.prompts import build_user_prompt, get_system_prompt
from autodocs_ai.core.renderer import render
from autodocs_ai.extractors import extract_file
from autodocs_ai.providers import GenerationResult, get_provider


@dataclass
class GenerateRequest:
    """Parameters for document generation."""

    prompt: str
    template: str | None = None
    output_path: str | None = None
    output_format: str = "pdf"
    input_files: list[str] = field(default_factory=list)
    language: str | None = None
    renderer: str | None = None
    provider: str | None = None


@dataclass
class GenerateResponse:
    """Result from document generation."""

    output_path: Path
    output_format: str
    ai_result: GenerationResult
    source_content: str


def _get_output_extension(output_format: str) -> str:
    """Get the file extension for an output format."""
    extensions = {
        "pdf": ".pdf",
        "docx": ".docx",
        "html": ".html",
        "markdown": ".md",
    }
    return extensions.get(output_format, ".pdf")


def _resolve_output_path(
    request: GenerateRequest, settings: Settings, fmt: str
) -> Path:
    """Determine the output file path."""
    if request.output_path:
        path = Path(request.output_path)
        if path.suffix:
            # If a specific file with extension, adjust extension for current format
            return path.with_suffix(_get_output_extension(fmt))
        return path / f"document{_get_output_extension(fmt)}"
    return settings.output_dir / f"document{_get_output_extension(fmt)}"


async def generate_document(
    request: GenerateRequest,
    settings: Settings | None = None,
) -> list[GenerateResponse]:
    """Generate a document from a prompt.

    This is the main orchestration function that:
    1. Extracts content from input files (if any)
    2. Builds the prompt with template instructions
    3. Calls the AI provider
    4. Renders the output in the requested format(s)

    Args:
        request: Generation parameters.
        settings: Optional settings override.

    Returns:
        List of GenerateResponse objects (one per output format).
    """
    if settings is None:
        overrides = {}
        if request.provider:
            overrides["provider"] = request.provider
        if request.language:
            overrides["language"] = request.language
        if request.renderer:
            overrides["renderer"] = request.renderer
        settings = get_settings(**overrides)

    # Extract content from input files
    input_content = None
    if request.input_files:
        extracted_parts = []
        for file_path in request.input_files:
            path = Path(file_path)
            if path.exists():
                content = extract_file(path)
                extracted_parts.append(f"--- {path.name} ---\n{content}")
        if extracted_parts:
            input_content = "\n\n".join(extracted_parts)

    # Parse output formats (supports comma-separated: "pdf,docx,html")
    formats = [f.strip() for f in request.output_format.split(",")]

    responses: list[GenerateResponse] = []
    # Cache AI results per format type to avoid duplicate calls
    ai_cache: dict[str, tuple[GenerationResult, str]] = {}

    for fmt in formats:
        # Determine the format-specific prompt type
        # pdf/typst and pdf/latex need different prompts, others are distinct
        if fmt == "pdf":
            prompt_key = settings.renderer.value
        else:
            prompt_key = fmt

        if prompt_key not in ai_cache:
            system_prompt = get_system_prompt(settings.renderer, fmt)
            user_prompt = build_user_prompt(
                prompt=request.prompt,
                template=request.template,
                language=settings.language,
                input_content=input_content,
            )

            provider = get_provider(settings)
            ai_result = await provider.generate(system_prompt, user_prompt)
            ai_cache[prompt_key] = (ai_result, ai_result.content)

        ai_result, source_content = ai_cache[prompt_key]
        output_path = _resolve_output_path(request, settings, fmt)

        rendered_path = render(
            source=source_content,
            output_path=output_path,
            renderer=settings.renderer,
            output_format=fmt,
        )

        responses.append(
            GenerateResponse(
                output_path=rendered_path,
                output_format=fmt,
                ai_result=ai_result,
                source_content=source_content,
            )
        )

    return responses
