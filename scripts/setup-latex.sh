#!/usr/bin/env bash
# Install TinyTeX for LaTeX support in autodocs-ai
set -euo pipefail

echo "Installing TinyTeX..."

if command -v pdflatex &> /dev/null; then
    echo "LaTeX is already installed."
    pdflatex --version | head -1
    exit 0
fi

OS="$(uname -s)"

case "${OS}" in
    Linux|Darwin)
        curl -fsSL https://yihui.org/tinytex/install-bin-unix.sh | sh
        ;;
    *)
        echo "Unsupported OS: ${OS}"
        echo "Please install TinyTeX manually: https://yihui.org/tinytex/"
        exit 1
        ;;
esac

# Install commonly needed LaTeX packages
echo "Installing common LaTeX packages..."
if command -v tlmgr &> /dev/null; then
    tlmgr install \
        amsmath \
        amssymb \
        booktabs \
        graphicx \
        hyperref \
        IEEEtran \
        geometry \
        fancyhdr \
        titlesec \
        enumitem \
        xcolor \
        listings \
        float
fi

echo "TinyTeX installed successfully."
pdflatex --version | head -1
