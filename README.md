<div align="center">

<!-- Hero Section -->
<img src="https://img.icons8.com/fluency/96/documents.png" alt="autodocs-ai logo" width="96" height="96" />

# autodocs-ai

### Prompt &rarr; Beautiful Document. One Command.

The **first open-source AI document generator** that turns a simple prompt into<br/>
professionally formatted **PDF, DOCX, HTML, and Markdown** documents.

<br/>

[![PyPI version](https://img.shields.io/pypi/v/autodocs-ai?style=for-the-badge&logo=pypi&logoColor=white&color=0073b7)](https://pypi.org/project/autodocs-ai/)
[![Python](https://img.shields.io/badge/python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-48%20passed-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](tests/)
[![AI Tests](https://img.shields.io/badge/AI%20tests-120%2F120-brightgreen?style=for-the-badge&logo=openai&logoColor=white)](#test-results)

<br/>

[Quick Start](#-quick-start) &bull;
[Features](#-features) &bull;
[Templates](#-8-built-in-templates) &bull;
[API](#-rest-api) &bull;
[Docker](#-docker) &bull;
[Contributing](#-contributing)

<br/>

---

</div>

<br/>

## The Problem

Every developer and professional has faced this: you need a polished document &mdash; a proposal, invoice, resume, report &mdash; and the options are:

- **Write it manually** in Word/Google Docs (slow, tedious)
- **Use a template engine** like Carbone or Docxtemplater (you still write all the content)
- **Use Pandoc/Typst/LaTeX** (you need to learn markup languages)
- **Use ChatGPT** and manually copy-paste into a formatter (fragmented workflow)

**None of these go from prompt to finished document in one step.**

<br/>

<div align="center">

### autodocs-ai fills the gap

| Category | Existing Tools | AI-Powered? |
|:---------|:--------------|:-----------:|
| Doc &rarr; Markdown (input) | Marker, MarkItDown | &check; |
| Format &rarr; Format (conversion) | Pandoc | &cross; |
| Markup &rarr; PDF (typesetting) | Typst, LaTeX | &cross; |
| Data + Template &rarr; Doc | Carbone, Docxtemplater | &cross; |
| **Prompt &rarr; Polished Document** | **autodocs-ai** | **&check;** |

</div>

<br/>

## &raquo; Quick Start

### 1. Install

```bash
pip install autodocs-ai[all]
```

<details>
<summary><b>Or install with only the provider you need</b></summary>
<br/>

```bash
pip install autodocs-ai[openai]       # OpenAI GPT models
pip install autodocs-ai[anthropic]    # Anthropic Claude
pip install autodocs-ai[gemini]       # Google Gemini
pip install autodocs-ai[ollama]       # Local models (free, no API key)
```

</details>

### 2. Configure

```bash
cp .env.example .env

# Set your provider and API key (pick one)
export AUTODOCS_PROVIDER=openai
export OPENAI_API_KEY=sk-...

# Or use Anthropic
export AUTODOCS_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# Or use Ollama (free, runs locally)
export AUTODOCS_PROVIDER=ollama
```

### 3. Set Up Rendering

```bash
autodocs setup             # Install Typst (fast, recommended)
autodocs setup --latex     # Also install LaTeX (for academic papers)
```

### 4. Generate!

```bash
# One command. That's it.
autodocs generate "Create a project proposal for a mobile fitness app" \
  --template proposal \
  --output proposal.pdf
```

<br/>

<div align="center">

```
  Prompt                    AI Engine                 Renderer              Output
+-----------+          +---------------+          +------------+        +----------+
|  "Create  |  ------> |  GPT-5.1 /    |  ------> |   Typst /  | -----> |  .pdf    |
|   a pro-  |          |  Claude /     |          |   LaTeX /  |        |  .docx   |
|   posal"  |          |  Gemini /     |          |   Direct   |        |  .html   |
|           |          |  Ollama       |          |            |        |  .md     |
+-----------+          +---------------+          +------------+        +----------+
```

</div>

<br/>

---

<br/>

## &star; Features

<table>
<tr>
<td width="50%" valign="top">

### &nbsp; 5 AI Providers

Connect to any major AI provider or run locally for free:

| Provider | Models | Auth |
|:---------|:-------|:-----|
| **OpenAI** | GPT-4o, GPT-5.1 | `OPENAI_API_KEY` |
| **Anthropic** | Claude Sonnet/Opus | `ANTHROPIC_API_KEY` |
| **Google Gemini** | Gemini 2.0 Flash | `GOOGLE_API_KEY` |
| **Azure OpenAI** | Any deployment | `AZURE_OPENAI_*` |
| **Ollama** | Llama, Mistral, etc. | Free, local |

</td>
<td width="50%" valign="top">

### &nbsp; 4 Output Formats

Generate one or many formats in a single command:

```bash
--format pdf        # Typst or LaTeX
--format docx       # Microsoft Word
--format html       # Standalone + CSS
--format markdown   # Clean Markdown

# Multiple at once:
--format pdf,docx,html
```

</td>
</tr>
<tr>
<td width="50%" valign="top">

### &nbsp; Dual Rendering Engine

- **Typst** (default) &mdash; Modern, fast (27x faster than LaTeX), ~40MB
- **LaTeX** &mdash; For academic papers (IEEE, ACM formatting)

Auto-selects Typst by default. Use `--renderer latex` for academic templates.

</td>
<td width="50%" valign="top">

### &nbsp; File Input Extraction

Feed existing files as context for the AI:

```bash
autodocs generate "Summarize into a report" \
  --input data.xlsx notes.md paper.pdf
```

**Supported:** PDF, Excel, CSV, Word, Markdown, code files, plain text

</td>
</tr>
<tr>
<td width="50%" valign="top">

### &nbsp; Beautiful CLI

Built with [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/) for a delightful terminal experience:

- Progress spinners during generation
- Colored, formatted output
- `--json` flag for machine-readable results
- Respects `NO_COLOR` env variable

</td>
<td width="50%" valign="top">

### &nbsp; REST API + Docker

Full FastAPI server with auto-generated OpenAPI docs:

```bash
autodocs serve   # http://localhost:8000
```

Or run everything in Docker:

```bash
docker compose -f docker/docker-compose.yml up
```

</td>
</tr>
</table>

<br/>

---

<br/>

## &page_facing_up; 8 Built-in Templates

Every template defines **document structure and intent** &mdash; not just layout. The AI understands what sections each document type needs.

<table>
<tr>
<td align="center" width="25%">
<br/>
<img src="https://img.icons8.com/fluency/48/resume.png" width="40" /><br/>
<b>Resume / CV</b><br/>
<sub>Contact, Summary, Experience,<br/>Education, Skills, Projects</sub>
<br/><br/>
</td>
<td align="center" width="25%">
<br/>
<img src="https://img.icons8.com/fluency/48/bill.png" width="40" /><br/>
<b>Invoice</b><br/>
<sub>Line items, Tax, Totals,<br/>Payment terms, Due dates</sub>
<br/><br/>
</td>
<td align="center" width="25%">
<br/>
<img src="https://img.icons8.com/fluency/48/business-report.png" width="40" /><br/>
<b>Business Proposal</b><br/>
<sub>Executive summary, Solution,<br/>Timeline, Budget, Next steps</sub>
<br/><br/>
</td>
<td align="center" width="25%">
<br/>
<img src="https://img.icons8.com/fluency/48/report-card.png" width="40" /><br/>
<b>Technical Report</b><br/>
<sub>Title page, TOC, Methodology,<br/>Findings, Recommendations</sub>
<br/><br/>
</td>
</tr>
<tr>
<td align="center" width="25%">
<br/>
<img src="https://img.icons8.com/fluency/48/graduation-cap.png" width="40" /><br/>
<b>Research Paper</b><br/>
<sub>Abstract, Literature review,<br/>Methodology, Results, Refs</sub>
<br/><br/>
</td>
<td align="center" width="25%">
<br/>
<img src="https://img.icons8.com/fluency/48/email-open.png" width="40" /><br/>
<b>Cover Letter</b><br/>
<sub>Header, Greeting, Qualifications,<br/>Call to action, Signature</sub>
<br/><br/>
</td>
<td align="center" width="25%">
<br/>
<img src="https://img.icons8.com/fluency/48/notepad.png" width="40" /><br/>
<b>Meeting Notes</b><br/>
<sub>Attendees, Agenda, Discussion,<br/>Decisions, Action items</sub>
<br/><br/>
</td>
<td align="center" width="25%">
<br/>
<img src="https://img.icons8.com/fluency/48/goal.png" width="40" /><br/>
<b>Project Charter</b><br/>
<sub>Objectives, Scope, Stakeholders,<br/>Milestones, Risks, Budget</sub>
<br/><br/>
</td>
</tr>
</table>

<br/>

### Usage Examples

```bash
# Professional resume
autodocs generate "Senior Python developer, 8 years at Google and Meta, \
  ML expertise, Stanford CS degree" --template resume --format pdf,docx

# Client invoice
autodocs generate "Invoice for Acme Corp: website redesign $8000, \
  SEO optimization $3000, monthly hosting $500" --template invoice -o invoice.pdf

# From existing files
autodocs generate "Create a quarterly report from this data" \
  --template report --input sales.xlsx notes.md -o Q4_report.pdf

# Academic paper
autodocs generate "Impact of LLMs on software engineering practices" \
  --template research_paper --renderer latex -o paper.pdf

# Multi-language
autodocs generate "Erstellen Sie einen Projektvorschlag fuer eine Fitness-App" \
  --template proposal --language german -o vorschlag.pdf
```

<br/>

---

<br/>

## &electric_plug; REST API

Start the server and generate documents programmatically:

```bash
autodocs serve --port 8000
```

### Endpoints

| Method | Endpoint | Description |
|:-------|:---------|:------------|
| `POST` | `/generate` | Generate a document and get metadata |
| `POST` | `/generate/download` | Generate and download the file |
| `GET` | `/health` | Health check |
| `GET` | `/templates` | List available templates |
| `GET` | `/providers` | List configured AI providers |

### Example

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create an invoice for web design services totaling $5000",
    "template": "invoice",
    "output_format": "html"
  }'
```

### API Key Authentication

Set `AUTODOCS_API_KEY` in your `.env` to require authentication:

```bash
curl -X POST http://localhost:8000/generate \
  -H "X-API-Key: your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "...", "template": "report"}'
```

Auto-generated **OpenAPI/Swagger docs** at `http://localhost:8000/docs`

<br/>

---

<br/>

## &whale; Docker

Zero-config deployment with everything bundled:

```bash
# Build and run
docker compose -f docker/docker-compose.yml up

# Or run directly
docker build -t autodocs-ai -f docker/Dockerfile .
docker run -v ./output:/output -p 8000:8000 --env-file .env autodocs-ai
```

<br/>

---

<br/>

## &keyboard; CLI Reference

```
USAGE
  autodocs <command> [options]

COMMANDS
  generate <prompt>          Generate a document from a prompt
    -t, --template NAME      Template: resume, invoice, proposal, report,
                             research_paper, cover_letter, meeting_notes,
                             project_charter
    -o, --output PATH        Output file path (default: ./output/document.ext)
    -f, --format FORMAT      Output format: pdf, docx, html, markdown
                             Comma-separate for multiple: pdf,docx,html
    -i, --input FILE         Input files to incorporate (repeatable)
    -l, --language LANG      Document language (default: english)
    -r, --renderer ENGINE    Rendering engine: typst (default) or latex
    -p, --provider NAME      AI provider: openai, anthropic, gemini, azure, ollama
        --json               Output result as JSON

  serve                      Start the REST API server
    -h, --host HOST          Server host (default: 0.0.0.0)
    -p, --port PORT          Server port (default: 8000)
        --reload             Enable auto-reload for development

  setup                      Install rendering dependencies
        --latex              Also install TinyTeX for LaTeX support

  check                      Verify all dependencies are configured
  templates                  List available document templates
  --version                  Show version
```

<br/>

---

<br/>

## &bar_chart; Comparison

<div align="center">

| Feature | autodocs-ai | Pandoc | Typst | Carbone | Synapsy Write |
|:--------|:-----------:|:------:|:-----:|:-------:|:-------------:|
| AI-powered content | &check; 5 providers | &cross; | &cross; | &cross; | &check; limited |
| One-command generation | &check; | Needs config | Needs markup | Needs template | &cross; No CLI |
| Built-in templates | 8+ semantic | 1 default | Community | Manual | &cross; |
| Multi-format output | PDF/DOCX/HTML/MD | &check; | PDF only | &check; | &cross; |
| CLI + REST API | Both | CLI only | CLI only | API only | Web only |
| Local AI (Ollama) | &check; Free | N/A | N/A | N/A | &cross; |
| File input extraction | &check; 6 formats | &cross; | &cross; | &cross; | &cross; |
| Docker image | &check; | Community | &cross; | &check; | &cross; |
| Multi-language docs | &check; Any language | &cross; | &cross; | &cross; | &cross; |
| API key auth | &check; | N/A | N/A | &check; | &check; |

</div>

<br/>

---

<br/>

## &test_tube; Test Results

Tested on **Azure Server** with **GPT-5.1-chat**:

<table>
<tr>
<td width="50%" valign="top">

### Unit Tests (pytest)

```
Run 1/5: 48/48 passed
Run 2/5: 48/48 passed
Run 3/5: 48/48 passed
Run 4/5: 48/48 passed
Run 5/5: 48/48 passed
```

**240 / 240 test executions passed**

</td>
<td width="50%" valign="top">

### AI Generation Tests

All 8 templates &times; 3 formats &times; 5 runs:

```
120 / 120 passed   (0 failures)
```

| Format | Pass Rate |
|:-------|:---------:|
| HTML | 40/40 (100%) |
| Markdown | 40/40 (100%) |
| DOCX | 40/40 (100%) |

</td>
</tr>
</table>

<br/>

---

<br/>

## &building_construction; Architecture

```
autodocs-ai/
  autodocs_ai/
    cli.py                     # Typer CLI (generate, serve, setup, check)
    config.py                  # Pydantic Settings (env + .env)
    api/
      app.py                   # FastAPI application
      models.py                # Request/Response schemas
      routes/
        documents.py           # POST /generate, /generate/download
        health.py              # GET /health, /templates, /providers
    providers/
      base.py                  # Abstract AIProvider
      openai_provider.py       # OpenAI Chat Completions
      anthropic_provider.py    # Anthropic Messages API
      gemini_provider.py       # Google Gemini
      azure_provider.py        # Azure OpenAI Service
      ollama_provider.py       # Ollama (local)
    core/
      generator.py             # Orchestrator: extract -> prompt -> AI -> render
      prompts.py               # System prompts + template instructions
      renderer.py              # Typst / LaTeX / HTML / DOCX / Markdown
    extractors/
      pdf.py, excel.py         # PDF, Excel/CSV extraction
      word.py, text.py         # Word, text/code extraction
    templates/
      resume.typ               # Typst templates
      invoice.typ, proposal.typ, report.typ
      research_paper.tex       # LaTeX template (IEEE)
    utils/
      mermaid.py               # Mermaid diagram rendering
      citations.py             # Auto-citation engine (APA/MLA/Chicago/IEEE)
      versioning.py            # Git-based document versioning
  tests/                       # 48 tests across 5 test files
  scripts/                     # Setup scripts (Typst, LaTeX)
  docker/                      # Dockerfile + docker-compose
```

<br/>

---

<br/>

## &gear; Configuration

All configuration via environment variables or `.env` file:

```bash
# Provider
AUTODOCS_PROVIDER=openai          # openai | anthropic | gemini | azure | ollama

# API Keys (set the one matching your provider)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AI...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://....openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Rendering
AUTODOCS_RENDERER=typst           # typst | latex

# Output
AUTODOCS_OUTPUT_DIR=./output
AUTODOCS_LANGUAGE=english
AUTODOCS_MAX_TOKENS=4096

# API Server
AUTODOCS_API_HOST=0.0.0.0
AUTODOCS_API_PORT=8000
AUTODOCS_API_KEY=                  # Set to enable API authentication
```

<br/>

---

<br/>

## &handshake; Contributing

We welcome contributions! See the [Contributing Guide](CONTRIBUTING.md) for details.

```bash
# Development setup
git clone https://github.com/makieali/autodocs-ai.git
cd autodocs-ai
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

# Run tests
pytest tests/ -v

# Lint
ruff check autodocs_ai/ tests/
ruff format autodocs_ai/ tests/
```

### Ways to Contribute

- **Add a new AI provider** &mdash; Implement `AIProvider` in `providers/`
- **Create a template** &mdash; Add a `.typ` file to `templates/`
- **Add a file extractor** &mdash; Implement `FileExtractor` in `extractors/`
- **Improve prompts** &mdash; Tune system prompts in `core/prompts.py`
- **Report bugs** &mdash; Open an issue

<br/>

---

<br/>

<div align="center">

## &rocket; Get Started

```bash
pip install autodocs-ai[all]
autodocs generate "Create a professional resume for a software engineer" --template resume -o resume.pdf
```

<br/>

**[View on PyPI](https://pypi.org/project/autodocs-ai/)** &bull;
**[Report a Bug](https://github.com/makieali/autodocs-ai/issues)** &bull;
**[Contributing Guide](CONTRIBUTING.md)**

<br/>

MIT License &copy; 2026 autodocs-ai contributors

<br/>

</div>
