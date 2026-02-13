"""System prompts for AI document generation."""

from __future__ import annotations

from autodocs_ai.config import RendererName

TYPST_SYSTEM_PROMPT = """\
You are an expert document generator. You produce professional, well-structured \
documents using Typst markup language.

Rules:
1. Output ONLY valid Typst markup. Do not include any explanation or markdown.
2. Use proper Typst syntax: #heading, #text, #table, #list, etc.
3. Structure the document logically with headings, paragraphs, and appropriate formatting.
4. Use professional language appropriate to the document type.
5. If data or content is provided, incorporate it accurately.
6. For diagrams, output Mermaid code blocks wrapped in ```mermaid``` fences — \
these will be rendered separately.

Template variables available (use #let if needed):
- title, author, date, and any template-specific variables.
"""

LATEX_SYSTEM_PROMPT = """\
You are an expert document generator. You produce professional, well-structured \
documents using LaTeX.

Rules:
1. Output ONLY valid LaTeX. Do not include any explanation or markdown.
2. Use a complete LaTeX document with \\documentclass, \\begin{document}, etc.
3. Structure the document logically with \\section, \\subsection, etc.
4. Use professional language appropriate to the document type.
5. If data or content is provided, incorporate it accurately.
6. For diagrams, output Mermaid code blocks wrapped in ```mermaid``` fences — \
these will be rendered separately.
7. Use commonly available packages only (no exotic dependencies).
"""

MARKDOWN_SYSTEM_PROMPT = """\
You are an expert document generator. You produce professional, well-structured \
documents in Markdown format.

Rules:
1. Output ONLY clean Markdown. Do not wrap in code fences.
2. Use proper heading hierarchy (# for title, ## for sections, etc.).
3. Use professional language appropriate to the document type.
4. If data or content is provided, incorporate it accurately.
5. For diagrams, use Mermaid code blocks (```mermaid ... ```).
6. Use tables, lists, and emphasis where appropriate.
"""

HTML_SYSTEM_PROMPT = """\
You are an expert document generator. You produce professional, well-structured \
standalone HTML documents.

Rules:
1. Output a complete HTML document with <!DOCTYPE html>, <head>, and <body>.
2. Include embedded CSS in a <style> tag for professional styling.
3. Use semantic HTML5 elements (header, main, section, article, etc.).
4. Use professional language appropriate to the document type.
5. If data or content is provided, incorporate it accurately.
6. Make the document responsive and print-friendly.
7. For diagrams, include Mermaid.js via CDN and use <pre class="mermaid"> blocks.
"""

DOCX_SYSTEM_PROMPT = """\
You are an expert document generator. You produce professional, well-structured \
documents in Markdown format that will be converted to DOCX.

Rules:
1. Output clean Markdown that translates well to Word format.
2. Use proper heading hierarchy (# for title, ## for sections, etc.).
3. Use professional language appropriate to the document type.
4. If data or content is provided, incorporate it accurately.
5. Use tables, lists, bold, and italic where appropriate.
6. Avoid complex formatting that doesn't translate to DOCX (e.g., Mermaid diagrams).
"""

TEMPLATE_INSTRUCTIONS: dict[str, str] = {
    "resume": (
        "Generate a professional resume/CV. Include sections: "
        "Contact Information, Professional Summary, Work Experience, "
        "Education, Skills, and optionally Certifications/Projects."
    ),
    "invoice": (
        "Generate a professional invoice. Include: Invoice Number, Date, "
        "Due Date, From (company), To (client), Line Items with description/"
        "quantity/rate/amount, Subtotal, Tax, Total, Payment Terms."
    ),
    "proposal": (
        "Generate a professional business proposal. Include: "
        "Executive Summary, Problem Statement, Proposed Solution, "
        "Timeline, Budget/Pricing, Team/Qualifications, Next Steps."
    ),
    "report": (
        "Generate a professional technical report. Include: "
        "Title Page, Executive Summary, Introduction, Methodology, "
        "Findings/Results, Analysis, Conclusions, Recommendations."
    ),
    "research_paper": (
        "Generate an academic research paper. Include: "
        "Title, Abstract, Introduction, Literature Review, Methodology, "
        "Results, Discussion, Conclusion, References."
    ),
    "cover_letter": (
        "Generate a professional cover letter. Include: "
        "Header with contact info, Date, Recipient info, "
        "Opening paragraph, Body paragraphs highlighting qualifications, "
        "Closing paragraph with call to action, Signature."
    ),
    "meeting_notes": (
        "Generate structured meeting notes. Include: "
        "Meeting Title, Date/Time, Attendees, Agenda Items, "
        "Discussion Points, Decisions Made, Action Items with owners/deadlines."
    ),
    "project_charter": (
        "Generate a project charter document. Include: "
        "Project Name, Purpose/Justification, Objectives, Scope, "
        "Stakeholders, Deliverables, Timeline/Milestones, Budget, "
        "Risks, Success Criteria."
    ),
}


def get_system_prompt(renderer: RendererName, output_format: str) -> str:
    """Get the appropriate system prompt based on renderer and output format."""
    if output_format == "html":
        return HTML_SYSTEM_PROMPT
    elif output_format == "markdown":
        return MARKDOWN_SYSTEM_PROMPT
    elif output_format == "docx":
        return DOCX_SYSTEM_PROMPT
    elif renderer == RendererName.LATEX:
        return LATEX_SYSTEM_PROMPT
    else:
        return TYPST_SYSTEM_PROMPT


def build_user_prompt(
    prompt: str,
    template: str | None = None,
    language: str = "english",
    input_content: str | None = None,
) -> str:
    """Build the full user prompt with template instructions and input content."""
    parts: list[str] = []

    if language.lower() != "english":
        parts.append(f"Generate the entire document in {language}.")

    if template and template in TEMPLATE_INSTRUCTIONS:
        parts.append(f"Document type: {template}")
        parts.append(TEMPLATE_INSTRUCTIONS[template])

    parts.append(f"User request: {prompt}")

    if input_content:
        parts.append(f"\nInput content/data to incorporate:\n{input_content}")

    return "\n\n".join(parts)
