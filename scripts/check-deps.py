#!/usr/bin/env python3
"""Check that all autodocs-ai dependencies are properly installed."""

from __future__ import annotations

import shutil
import sys


def check(name: str, check_fn) -> bool:
    """Run a check and print the result."""
    try:
        result = check_fn()
        print(f"  ✓ {name}: {result}")
        return True
    except Exception as e:
        print(f"  ✗ {name}: {e}")
        return False


def main() -> int:
    print("autodocs-ai dependency check\n")
    all_ok = True

    # Python
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Python: {py_ver}")
    if sys.version_info < (3, 10):
        print("  ✗ Python 3.10+ required")
        all_ok = False

    # Core packages
    print("\nCore packages:")
    for pkg in ["typer", "rich", "pydantic", "pydantic_settings", "httpx"]:
        if not check(pkg, lambda p=pkg: __import__(p).__version__ if hasattr(__import__(p), "__version__") else "installed"):
            all_ok = False

    # AI Providers
    print("\nAI Providers:")
    for pkg, name in [("openai", "OpenAI"), ("anthropic", "Anthropic"), ("google.genai", "Gemini"), ("ollama", "Ollama")]:
        check(name, lambda p=pkg: __import__(p) and "installed")

    # Rendering
    print("\nRendering:")
    check("Typst CLI", lambda: shutil.which("typst") or "not found")
    check("Typst Python", lambda: __import__("typst") and "installed")
    check("LaTeX", lambda: shutil.which("pdflatex") or "not found")

    # Extractors
    print("\nExtractors:")
    for pkg, name in [("PyPDF2", "PDF"), ("docx", "Word"), ("pandas", "Excel/CSV")]:
        check(name, lambda p=pkg: __import__(p) and "installed")

    # API
    print("\nAPI:")
    for pkg in ["fastapi", "uvicorn"]:
        check(pkg, lambda p=pkg: __import__(p) and "installed")

    print()
    if all_ok:
        print("All core dependencies OK!")
    else:
        print("Some dependencies are missing. See above for details.")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
