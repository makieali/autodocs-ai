# autodocs-ai

**AI-powered document generator. Prompt to beautiful PDF/DOCX/HTML in one command.**

[![CI](https://github.com/autodocs-ai/autodocs-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/autodocs-ai/autodocs-ai/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/autodocs-ai)](https://pypi.org/project/autodocs-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## What is autodocs-ai?

autodocs-ai takes a prompt (or files) and generates professionally formatted documents. One command. No templates to fill, no markup to write.

```bash
# Generate a PDF from a prompt
autodocs generate "Create a project proposal for a mobile fitness app" --template proposal --output proposal.pdf

# Generate from existing files
autodocs generate "Summarize this data into a report" --input data.csv notes.md --template report --output report.pdf

# Multiple output formats at once
autodocs generate "Create my resume" --template resume --format pdf,docx,html

# Start the API server
autodocs serve
```

## The Gap We Fill

| Category | Existing Tools | AI-Powered? |
|----------|---------------|-------------|
| Doc to Markdown (input) | Marker, MarkItDown | Yes |
| Format to Format (conversion) | Pandoc | No |
| Markup to PDF (typesetting) | Typst, LaTeX | No |
| Data + Template to Doc | Carbone, Docxtemplater | No |
| **Prompt to Polished Document** | **autodocs-ai** | **Yes** |

## Quick Start

### Install

```bash
pip install autodocs-ai[all]
```

Or install with specific providers:

```bash
pip install autodocs-ai[openai]      # OpenAI only
pip install autodocs-ai[anthropic]   # Claude only
pip install autodocs-ai[ollama]      # Local models (free)
```

### Configure

```bash
# Copy the template
cp .env.example .env

# Set your API key (pick one)
export OPENAI_API_KEY=sk-...
# or
export ANTHROPIC_API_KEY=sk-ant-...
# or use Ollama for free local models
export AUTODOCS_PROVIDER=ollama
```

### Set Up Rendering

```bash
# Install Typst (fast, recommended)
autodocs setup

# Or install LaTeX (for academic papers)
autodocs setup --latex
```

### Generate

```bash
autodocs generate "Write a cover letter for a senior Python developer position at Google" \
  --template cover_letter \
  --output cover_letter.pdf
```

## Features

### 5 AI Providers

| Provider | Model | Setup |
|----------|-------|-------|
| **OpenAI** | GPT-4o | `OPENAI_API_KEY` |
| **Anthropic** | Claude Sonnet | `ANTHROPIC_API_KEY` |
| **Google Gemini** | Gemini 2.0 Flash | `GOOGLE_API_KEY` |
| **Azure OpenAI** | Any deployed model | `AZURE_OPENAI_*` |
| **Ollama** | Llama 3.1, Mistral, etc. | Local, free |

### 8 Built-in Templates

- **Resume/CV** — Professional resume with sections for experience, education, skills
- **Invoice** — Complete invoice with line items, tax, and totals
- **Business Proposal** — Executive summary, timeline, budget, and next steps
- **Technical Report** — Full report with table of contents and analysis
- **Research Paper** — IEEE/ACM format with abstract, methodology, and references
- **Cover Letter** — Professional letter tailored to the position
- **Meeting Notes** — Structured notes with action items and decisions
- **Project Charter** — Complete charter with scope, risks, and success criteria

### 4 Output Formats

```bash
--format pdf        # Via Typst (fast) or LaTeX (academic)
--format docx       # Microsoft Word
--format html       # Standalone HTML with embedded CSS
--format markdown   # Clean Markdown
--format pdf,docx   # Multiple formats at once
```

### Dual Rendering Engine

- **Typst** (default) — 40MB binary, 27x faster than LaTeX, modern syntax
- **LaTeX** — For academic papers requiring IEEE/ACM formatting

### File Input Extraction

Feed existing files to the AI for context:

```bash
autodocs generate "Create a summary report" \
  --input quarterly_data.xlsx meeting_notes.md research.pdf
```

Supported: PDF, Excel (.xlsx/.csv), Word (.docx), Markdown, code files, and plain text.

### REST API

```bash
autodocs serve  # Starts on http://localhost:8000

# Generate via API
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create an invoice for web design services", "template": "invoice"}'
```

Auto-generated docs at `http://localhost:8000/docs`.

### Docker

```bash
docker compose -f docker/docker-compose.yml up
```

## CLI Reference

```
autodocs generate <prompt>     Generate a document
  --template, -t              Template name
  --output, -o                Output file path
  --format, -f                Output format (pdf, docx, html, markdown)
  --input, -i                 Input files (repeatable)
  --language, -l              Document language
  --renderer, -r              Rendering engine (typst, latex)
  --provider, -p              AI provider override
  --json                      Output result as JSON

autodocs serve                 Start the API server
  --host, -h                  Server host (default: 0.0.0.0)
  --port, -p                  Server port (default: 8000)
  --reload                    Enable auto-reload

autodocs setup                 Install rendering dependencies
  --latex                     Also install TinyTeX

autodocs check                 Verify all dependencies
autodocs templates             List available templates
```

## Comparison

| Feature | autodocs-ai | Pandoc | Typst | Carbone |
|---------|-------------|--------|-------|---------|
| AI-powered content | Yes (5 providers) | No | No | No |
| One-command PDF | Yes | Needs config | Needs markup | Needs template |
| Built-in templates | 8+ | 1 default | Community | Manual |
| Multi-format output | PDF/DOCX/HTML/MD | Yes | PDF only | Yes |
| CLI + API | Both | CLI only | CLI only | API only |
| Local AI (Ollama) | Yes | N/A | N/A | N/A |
| Docker image | Yes | Community | No | Yes |
| File input extraction | Yes | No | No | No |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT
