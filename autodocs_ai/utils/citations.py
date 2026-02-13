"""Auto-citation engine for generating bibliographies from URLs."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Citation:
    """A single citation entry."""

    url: str
    title: str = ""
    author: str = ""
    date: str = ""
    publisher: str = ""
    accessed: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))


class CitationStyle:
    """Format citations in different academic styles."""

    @staticmethod
    def format_apa(citation: Citation) -> str:
        """Format citation in APA style."""
        parts = []
        if citation.author:
            parts.append(f"{citation.author}")
        if citation.date:
            parts.append(f"({citation.date})")
        elif citation.accessed:
            parts.append(f"(n.d.)")
        if citation.title:
            parts.append(f"*{citation.title}*")
        if citation.publisher:
            parts.append(f"{citation.publisher}")
        parts.append(f"Retrieved {citation.accessed}, from {citation.url}")
        return ". ".join(parts) + "."

    @staticmethod
    def format_mla(citation: Citation) -> str:
        """Format citation in MLA style."""
        parts = []
        if citation.author:
            parts.append(f"{citation.author}.")
        if citation.title:
            parts.append(f'"{citation.title}."')
        if citation.publisher:
            parts.append(f"*{citation.publisher}*,")
        if citation.date:
            parts.append(f"{citation.date}.")
        parts.append(f"Web. {citation.accessed}.")
        return " ".join(parts)

    @staticmethod
    def format_chicago(citation: Citation) -> str:
        """Format citation in Chicago style."""
        parts = []
        if citation.author:
            parts.append(f"{citation.author}.")
        if citation.title:
            parts.append(f'"{citation.title}."')
        if citation.publisher:
            parts.append(f"{citation.publisher}.")
        if citation.date:
            parts.append(f"{citation.date}.")
        parts.append(f"Accessed {citation.accessed}. {citation.url}.")
        return " ".join(parts)

    @staticmethod
    def format_ieee(citation: Citation, index: int = 1) -> str:
        """Format citation in IEEE style."""
        parts = [f"[{index}]"]
        if citation.author:
            parts.append(f"{citation.author},")
        if citation.title:
            parts.append(f'"{citation.title},"')
        if citation.publisher:
            parts.append(f"{citation.publisher},")
        if citation.date:
            parts.append(f"{citation.date}.")
        parts.append(f"[Online]. Available: {citation.url}")
        parts.append(f"[Accessed: {citation.accessed}]")
        return " ".join(parts)


FORMATTERS = {
    "apa": CitationStyle.format_apa,
    "mla": CitationStyle.format_mla,
    "chicago": CitationStyle.format_chicago,
    "ieee": CitationStyle.format_ieee,
}


async def fetch_citation_metadata(url: str) -> Citation:
    """Fetch metadata from a URL to build a citation.

    Args:
        url: The URL to fetch metadata from.

    Returns:
        Citation object with available metadata.
    """
    import httpx

    citation = Citation(url=url)

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
            response = await client.get(url)
            html = response.text

            # Extract title
            title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
            if title_match:
                citation.title = title_match.group(1).strip()

            # Extract meta author
            author_match = re.search(
                r'<meta[^>]+name=["\']author["\'][^>]+content=["\'](.*?)["\']',
                html,
                re.IGNORECASE,
            )
            if author_match:
                citation.author = author_match.group(1).strip()

            # Extract meta date
            date_match = re.search(
                r'<meta[^>]+(?:name|property)=["\'](?:date|article:published_time)["\']'
                r'[^>]+content=["\'](.*?)["\']',
                html,
                re.IGNORECASE,
            )
            if date_match:
                citation.date = date_match.group(1).strip()

            # Extract publisher / site name
            site_match = re.search(
                r'<meta[^>]+property=["\']og:site_name["\'][^>]+content=["\'](.*?)["\']',
                html,
                re.IGNORECASE,
            )
            if site_match:
                citation.publisher = site_match.group(1).strip()

    except Exception:
        # If we can't fetch, return what we have (just the URL)
        pass

    return citation


def generate_bibliography(
    citations: list[Citation],
    style: str = "apa",
) -> str:
    """Generate a formatted bibliography from a list of citations.

    Args:
        citations: List of Citation objects.
        style: Citation style (apa, mla, chicago, ieee).

    Returns:
        Formatted bibliography string.
    """
    formatter = FORMATTERS.get(style.lower(), CitationStyle.format_apa)

    entries = []
    for i, citation in enumerate(citations, 1):
        if style == "ieee":
            entries.append(formatter(citation, i))
        else:
            entries.append(formatter(citation))

    return "\n\n".join(entries)
