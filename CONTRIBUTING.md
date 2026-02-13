# Contributing to autodocs-ai

Thanks for your interest in contributing! This guide will help you get started.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/autodocs-ai/autodocs-ai.git
cd autodocs-ai

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install with dev dependencies
pip install -e ".[dev]"

# Install Typst for PDF rendering
bash scripts/setup-typst.sh

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

## Running Tests

```bash
pytest tests/ -v
```

## Code Style

We use [ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
ruff check autodocs_ai/ tests/
ruff format autodocs_ai/ tests/
```

## How to Contribute

### Adding a New AI Provider

1. Create a new file in `autodocs_ai/providers/` (e.g., `my_provider.py`)
2. Implement the `AIProvider` abstract class from `autodocs_ai/providers/base.py`
3. Add the provider to `ProviderName` enum in `autodocs_ai/config.py`
4. Add the factory case in `autodocs_ai/providers/__init__.py`
5. Add configuration fields to `Settings` in `autodocs_ai/config.py`
6. Add tests in `tests/test_providers.py`
7. Update `.env.example` with new config options

### Adding a New Template

1. Create a `.typ` file in `autodocs_ai/templates/`
2. Add a template description to `TEMPLATE_INSTRUCTIONS` in `autodocs_ai/core/prompts.py`
3. Add the template name to `TemplateName` enum in `autodocs_ai/config.py`

### Adding a New File Extractor

1. Create a new file in `autodocs_ai/extractors/` (e.g., `my_format.py`)
2. Implement the `FileExtractor` abstract class
3. Register it in `autodocs_ai/extractors/__init__.py`
4. Add tests in `tests/test_extractors.py`

## Pull Request Process

1. Fork the repo and create a feature branch
2. Make your changes with tests
3. Run `ruff check` and `ruff format` to ensure code quality
4. Run `pytest` to ensure all tests pass
5. Submit a PR with a clear description of your changes

## Code of Conduct

Be kind, respectful, and constructive. We're all here to build something useful together.
