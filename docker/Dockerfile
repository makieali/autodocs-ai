FROM python:3.12-slim

LABEL maintainer="autodocs-ai contributors"
LABEL description="AI-powered document generator"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Typst
ARG TYPST_VERSION=0.12.0
RUN ARCH=$(dpkg --print-architecture) && \
    case ${ARCH} in \
        amd64) TARGET="x86_64-unknown-linux-musl" ;; \
        arm64) TARGET="aarch64-unknown-linux-musl" ;; \
        *) echo "Unsupported: ${ARCH}" && exit 1 ;; \
    esac && \
    curl -fsSL "https://github.com/typst/typst/releases/download/v${TYPST_VERSION}/typst-${TARGET}.tar.xz" \
    | tar xJ --strip-components=1 -C /usr/local/bin/ && \
    typst --version

# Set up app
WORKDIR /app

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir ".[all]"

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p /output

ENV AUTODOCS_OUTPUT_DIR=/output

EXPOSE 8000

# Default: run the API server
CMD ["autodocs", "serve", "--host", "0.0.0.0", "--port", "8000"]
