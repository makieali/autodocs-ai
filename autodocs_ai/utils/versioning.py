"""Git-based document versioning utility."""

from __future__ import annotations

import subprocess
from pathlib import Path


class VersioningError(Exception):
    """Raised when versioning operations fail."""


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run a git command in the given directory."""
    return subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=30,
    )


def init_versioning(output_dir: Path) -> None:
    """Initialize git repository in the output directory for document versioning.

    Args:
        output_dir: Directory to initialize git in.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    git_dir = output_dir / ".git"
    if git_dir.exists():
        return  # Already initialized

    result = _run_git(["init"], cwd=output_dir)
    if result.returncode != 0:
        raise VersioningError(f"Failed to initialize git: {result.stderr}")

    # Create initial commit
    _run_git(["commit", "--allow-empty", "-m", "Initialize document versioning"], cwd=output_dir)


def commit_version(
    output_dir: Path,
    message: str | None = None,
    files: list[str] | None = None,
) -> str | None:
    """Commit the current state of documents.

    Args:
        output_dir: The versioned output directory.
        message: Commit message. Auto-generated if not provided.
        files: Specific files to commit. If None, commits all changes.

    Returns:
        The commit hash, or None if nothing to commit.
    """
    git_dir = output_dir / ".git"
    if not git_dir.exists():
        init_versioning(output_dir)

    # Stage files
    if files:
        for f in files:
            _run_git(["add", f], cwd=output_dir)
    else:
        _run_git(["add", "-A"], cwd=output_dir)

    # Check if there's anything to commit
    status = _run_git(["status", "--porcelain"], cwd=output_dir)
    if not status.stdout.strip():
        return None

    if not message:
        message = "Update generated documents"

    result = _run_git(["commit", "-m", message], cwd=output_dir)
    if result.returncode != 0:
        raise VersioningError(f"Failed to commit: {result.stderr}")

    # Get the commit hash
    hash_result = _run_git(["rev-parse", "HEAD"], cwd=output_dir)
    return hash_result.stdout.strip() if hash_result.returncode == 0 else None


def list_versions(output_dir: Path, limit: int = 20) -> list[dict[str, str]]:
    """List document versions (git commits).

    Args:
        output_dir: The versioned output directory.
        limit: Maximum number of versions to return.

    Returns:
        List of version dicts with hash, date, and message.
    """
    git_dir = output_dir / ".git"
    if not git_dir.exists():
        return []

    result = _run_git(
        ["log", f"-{limit}", "--format=%H|%ai|%s"],
        cwd=output_dir,
    )
    if result.returncode != 0:
        return []

    versions = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) == 3:
            versions.append({
                "hash": parts[0],
                "date": parts[1],
                "message": parts[2],
            })
    return versions


def diff_versions(
    output_dir: Path,
    hash_a: str,
    hash_b: str | None = None,
) -> str:
    """Show diff between two versions, or between a version and current state.

    Args:
        output_dir: The versioned output directory.
        hash_a: First commit hash.
        hash_b: Second commit hash (if None, diffs against working directory).

    Returns:
        Diff output as string.
    """
    args = ["diff", hash_a]
    if hash_b:
        args.append(hash_b)

    result = _run_git(args, cwd=output_dir)
    return result.stdout


def restore_version(output_dir: Path, commit_hash: str) -> None:
    """Restore documents to a specific version.

    Args:
        output_dir: The versioned output directory.
        commit_hash: The commit hash to restore.
    """
    result = _run_git(["checkout", commit_hash, "--", "."], cwd=output_dir)
    if result.returncode != 0:
        raise VersioningError(f"Failed to restore version: {result.stderr}")
