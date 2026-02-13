#!/usr/bin/env bash
# Install Typst binary for autodocs-ai
set -euo pipefail

TYPST_VERSION="0.12.0"

echo "Installing Typst v${TYPST_VERSION}..."

OS="$(uname -s)"
ARCH="$(uname -m)"

case "${OS}" in
    Linux)
        case "${ARCH}" in
            x86_64)  TARGET="x86_64-unknown-linux-musl" ;;
            aarch64) TARGET="aarch64-unknown-linux-musl" ;;
            *)       echo "Unsupported architecture: ${ARCH}"; exit 1 ;;
        esac
        ;;
    Darwin)
        case "${ARCH}" in
            x86_64)  TARGET="x86_64-apple-darwin" ;;
            arm64)   TARGET="aarch64-apple-darwin" ;;
            *)       echo "Unsupported architecture: ${ARCH}"; exit 1 ;;
        esac
        ;;
    *)
        echo "Unsupported OS: ${OS}"
        echo "Please install Typst manually: https://github.com/typst/typst#installation"
        exit 1
        ;;
esac

URL="https://github.com/typst/typst/releases/download/v${TYPST_VERSION}/typst-${TARGET}.tar.xz"
INSTALL_DIR="${HOME}/.local/bin"

mkdir -p "${INSTALL_DIR}"

echo "Downloading from ${URL}..."
TMPDIR="$(mktemp -d)"
curl -fsSL "${URL}" | tar xJ -C "${TMPDIR}"

# Find the typst binary in the extracted archive
TYPST_BIN=$(find "${TMPDIR}" -name "typst" -type f | head -1)
if [ -z "${TYPST_BIN}" ]; then
    echo "Error: Could not find typst binary in archive"
    rm -rf "${TMPDIR}"
    exit 1
fi

cp "${TYPST_BIN}" "${INSTALL_DIR}/typst"
chmod +x "${INSTALL_DIR}/typst"
rm -rf "${TMPDIR}"

# Check if install dir is in PATH
if ! echo "${PATH}" | tr ':' '\n' | grep -q "^${INSTALL_DIR}$"; then
    echo ""
    echo "Add this to your shell profile:"
    echo "  export PATH=\"\${HOME}/.local/bin:\${PATH}\""
fi

echo "Typst v${TYPST_VERSION} installed to ${INSTALL_DIR}/typst"
"${INSTALL_DIR}/typst" --version
