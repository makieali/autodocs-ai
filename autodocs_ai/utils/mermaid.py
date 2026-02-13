"""Mermaid diagram rendering utility."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path


class MermaidError(Exception):
    """Raised when Mermaid rendering fails."""


def extract_mermaid_blocks(content: str) -> list[str]:
    """Extract Mermaid code blocks from document content.

    Args:
        content: Document source containing ```mermaid blocks.

    Returns:
        List of Mermaid diagram source strings.
    """
    pattern = r"```mermaid\s*\n(.*?)```"
    return re.findall(pattern, content, re.DOTALL)


def render_mermaid_to_svg(mermaid_source: str, output_path: Path | None = None) -> str:
    """Render a Mermaid diagram to SVG.

    Requires mmdc (Mermaid CLI) to be installed:
    npm install -g @mermaid-js/mermaid-cli

    Args:
        mermaid_source: Mermaid diagram source code.
        output_path: Optional path to save the SVG file.

    Returns:
        SVG content as a string.

    Raises:
        MermaidError: If rendering fails.
    """
    mmdc = shutil.which("mmdc")
    if not mmdc:
        raise MermaidError(
            "Mermaid CLI (mmdc) is not installed. "
            "Install with: npm install -g @mermaid-js/mermaid-cli"
        )

    with tempfile.NamedTemporaryFile(suffix=".mmd", mode="w", delete=False) as f:
        f.write(mermaid_source)
        f.flush()
        mmd_path = Path(f.name)

    svg_path = output_path or mmd_path.with_suffix(".svg")

    try:
        result = subprocess.run(
            [mmdc, "-i", str(mmd_path), "-o", str(svg_path), "-b", "transparent"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise MermaidError(f"Mermaid rendering failed:\n{result.stderr}")

        svg_content = svg_path.read_text()
        return svg_content
    finally:
        mmd_path.unlink(missing_ok=True)
        if output_path is None:
            svg_path.unlink(missing_ok=True)


def replace_mermaid_with_images(
    content: str,
    output_dir: Path,
    format: str = "svg",
) -> str:
    """Replace Mermaid code blocks with rendered image references.

    Args:
        content: Document source with ```mermaid blocks.
        output_dir: Directory to save rendered images.
        format: Output format (svg or png).

    Returns:
        Content with Mermaid blocks replaced by image references.
    """
    blocks = extract_mermaid_blocks(content)
    if not blocks:
        return content

    output_dir.mkdir(parents=True, exist_ok=True)

    for i, block in enumerate(blocks):
        try:
            img_path = output_dir / f"diagram_{i}.{format}"
            render_mermaid_to_svg(block, img_path)

            # Replace the mermaid block with an image reference
            old = f"```mermaid\n{block}```"
            if content.endswith(".typ") or "#" in content[:100]:
                # Typst image reference
                new = f'#image("{img_path}")'
            elif "\\begin" in content[:200]:
                # LaTeX image reference
                new = f"\\includegraphics[width=\\linewidth]{{{img_path}}}"
            else:
                # Markdown/HTML image reference
                new = f"![Diagram {i}]({img_path})"

            content = content.replace(old, new)
        except MermaidError:
            # Leave the mermaid block as-is if rendering fails
            continue

    return content
