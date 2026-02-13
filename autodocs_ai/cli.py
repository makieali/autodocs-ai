"""CLI interface using Typer with Rich output."""

from __future__ import annotations

import asyncio
import json
import shutil
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from autodocs_ai import __version__
from autodocs_ai.config import (
    OutputFormat,
    ProviderName,
    RendererName,
    TemplateName,
    get_settings,
)

app = typer.Typer(
    name="autodocs",
    help="AI-powered document generator. Prompt → Beautiful PDF/DOCX/HTML in one command.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)
console = Console()
err_console = Console(stderr=True)


def version_callback(value: bool) -> None:
    if value:
        console.print(f"autodocs-ai v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """autodocs-ai — AI-powered document generator."""


@app.command()
def generate(
    prompt: str = typer.Argument(..., help="The prompt describing the document to generate."),
    template: Optional[str] = typer.Option(
        None,
        "--template",
        "-t",
        help="Document template (resume, invoice, proposal, report, research_paper, "
        "cover_letter, meeting_notes, project_charter).",
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path. Defaults to ./output/document.<ext>",
    ),
    format: str = typer.Option(
        "pdf",
        "--format",
        "-f",
        help="Output format(s): pdf, docx, html, markdown. Comma-separate for multiple.",
    ),
    input_files: Optional[list[str]] = typer.Option(
        None,
        "--input",
        "-i",
        help="Input files to incorporate (PDF, Excel, Word, text, code).",
    ),
    language: Optional[str] = typer.Option(
        None,
        "--language",
        "-l",
        help="Document language (default: english).",
    ),
    renderer: Optional[str] = typer.Option(
        None,
        "--renderer",
        "-r",
        help="Rendering engine: typst or latex.",
    ),
    provider: Optional[str] = typer.Option(
        None,
        "--provider",
        "-p",
        help="AI provider: openai, anthropic, gemini, azure, ollama.",
    ),
    output_json: bool = typer.Option(
        False,
        "--json",
        help="Output result as JSON.",
    ),
) -> None:
    """Generate a document from a prompt."""
    from autodocs_ai.core.generator import GenerateRequest, generate_document

    request = GenerateRequest(
        prompt=prompt,
        template=template,
        output_path=output,
        output_format=format,
        input_files=input_files or [],
        language=language,
        renderer=renderer,
        provider=provider,
    )

    with console.status("[bold green]Generating document...", spinner="dots"):
        try:
            responses = asyncio.run(generate_document(request))
        except Exception as e:
            if output_json:
                console.print_json(json.dumps({"error": str(e)}))
            else:
                err_console.print(f"[bold red]Error:[/] {e}")
            raise typer.Exit(code=1)

    if output_json:
        results = []
        for r in responses:
            results.append({
                "output_path": str(r.output_path),
                "output_format": r.output_format,
                "model": r.ai_result.model,
                "provider": r.ai_result.provider,
                "usage": r.ai_result.usage,
            })
        console.print_json(json.dumps(results, indent=2))
    else:
        for r in responses:
            console.print(
                Panel(
                    f"[green]Generated:[/] {r.output_path}\n"
                    f"[dim]Format: {r.output_format} | "
                    f"Provider: {r.ai_result.provider} | "
                    f"Model: {r.ai_result.model}[/]",
                    title="[bold]autodocs-ai[/]",
                    border_style="green",
                )
            )


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Server host."),
    port: int = typer.Option(8000, "--port", "-p", help="Server port."),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload for development."),
) -> None:
    """Start the API server."""
    try:
        import uvicorn
    except ImportError:
        err_console.print(
            "[bold red]Error:[/] API dependencies not installed. "
            "Install with: pip install autodocs-ai[api]"
        )
        raise typer.Exit(code=1)

    console.print(
        Panel(
            f"Starting autodocs-ai API server on [bold]{host}:{port}[/]\n"
            f"Docs: http://{host}:{port}/docs",
            title="[bold]autodocs-ai server[/]",
            border_style="blue",
        )
    )

    uvicorn.run(
        "autodocs_ai.api.app:app",
        host=host,
        port=port,
        reload=reload,
    )


@app.command()
def setup(
    latex: bool = typer.Option(False, "--latex", help="Also install TinyTeX for LaTeX support."),
) -> None:
    """Set up rendering dependencies (Typst, optionally LaTeX)."""
    import subprocess

    # Check for Typst
    if shutil.which("typst"):
        console.print("[green]✓[/] Typst is already installed.")
    else:
        console.print("[yellow]Installing Typst...[/]")
        script_path = Path(__file__).parent.parent / "scripts" / "setup-typst.sh"
        if script_path.exists():
            result = subprocess.run(["bash", str(script_path)], capture_output=True, text=True)
            if result.returncode == 0:
                console.print("[green]✓[/] Typst installed successfully.")
            else:
                err_console.print(f"[red]✗[/] Failed to install Typst: {result.stderr}")
                console.print(
                    "[dim]Install manually: https://github.com/typst/typst#installation[/]"
                )
        else:
            console.print(
                "[yellow]Setup script not found.[/] "
                "Install Typst manually: https://github.com/typst/typst#installation"
            )

    # Check for Python typst bindings
    try:
        import typst  # noqa: F401

        console.print("[green]✓[/] Python typst bindings installed.")
    except ImportError:
        console.print(
            "[yellow]![/] Python typst bindings not installed. "
            "Install with: pip install typst"
        )

    if latex:
        if shutil.which("pdflatex"):
            console.print("[green]✓[/] LaTeX is already installed.")
        else:
            console.print("[yellow]Installing TinyTeX...[/]")
            script_path = Path(__file__).parent.parent / "scripts" / "setup-latex.sh"
            if script_path.exists():
                result = subprocess.run(
                    ["bash", str(script_path)], capture_output=True, text=True
                )
                if result.returncode == 0:
                    console.print("[green]✓[/] TinyTeX installed successfully.")
                else:
                    err_console.print(f"[red]✗[/] Failed to install TinyTeX: {result.stderr}")
            else:
                console.print(
                    "[yellow]Setup script not found.[/] "
                    "Install TinyTeX manually: https://yihui.org/tinytex/"
                )


@app.command()
def check() -> None:
    """Check that all dependencies are properly configured."""
    table = Table(title="autodocs-ai Dependency Check")
    table.add_column("Component", style="bold")
    table.add_column("Status")
    table.add_column("Details", style="dim")

    # Python version
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    table.add_row("Python", f"[green]✓[/] {py_ver}", "")

    # Typst
    if shutil.which("typst"):
        table.add_row("Typst CLI", "[green]✓[/] installed", shutil.which("typst") or "")
    else:
        table.add_row("Typst CLI", "[yellow]✗[/] not found", "Run: autodocs setup")

    try:
        import typst  # noqa: F401

        table.add_row("Typst Python", "[green]✓[/] installed", "")
    except ImportError:
        table.add_row("Typst Python", "[yellow]✗[/] not found", "pip install typst")

    # LaTeX
    if shutil.which("pdflatex"):
        table.add_row("LaTeX", "[green]✓[/] installed", shutil.which("pdflatex") or "")
    else:
        table.add_row("LaTeX", "[dim]✗[/] not found", "Optional: autodocs setup --latex")

    # AI Providers
    settings = get_settings()

    providers = [
        ("OpenAI", "openai", settings.openai_api_key),
        ("Anthropic", "anthropic", settings.anthropic_api_key),
        ("Gemini", "google-genai", settings.google_api_key),
        ("Ollama", "ollama", None),  # No key needed
    ]

    for name, pkg, key in providers:
        try:
            __import__(pkg.replace("-", "_") if "-" in pkg else pkg)
            pkg_ok = True
        except ImportError:
            pkg_ok = False

        if pkg_ok and (key or name == "Ollama"):
            table.add_row(name, "[green]✓[/] ready", "Package + key configured")
        elif pkg_ok:
            table.add_row(name, "[yellow]~[/] package only", "API key not set")
        else:
            table.add_row(name, "[dim]✗[/] not installed", f"pip install autodocs-ai[{pkg}]")

    # Active provider
    table.add_row("Active Provider", f"[bold]{settings.provider.value}[/]", "")

    console.print(table)


@app.command()
def templates() -> None:
    """List available document templates."""
    from autodocs_ai.core.prompts import TEMPLATE_INSTRUCTIONS

    table = Table(title="Available Templates")
    table.add_column("Name", style="bold")
    table.add_column("Description")

    for name, desc in TEMPLATE_INSTRUCTIONS.items():
        table.add_row(name, desc[:80] + "..." if len(desc) > 80 else desc)

    console.print(table)


if __name__ == "__main__":
    app()
