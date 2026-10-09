"""Safe, bounded HTML extraction for user-supplied public URLs."""
import ipaddress
import socket
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

USER_AGENT = "WebResearchQA/2.0 (+https://github.com/Simmisingh3/WEB_QuestionAnswering_Tool)"
MAX_REDIRECTS = 4


def _validate_public_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https URLs are supported.")
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Please provide a valid public URL without embedded credentials.")
    host = parsed.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
        raise ValueError("Local and internal URLs are not allowed.")
    try:
        addresses = [ipaddress.ip_address(host)]
    except ValueError:
        try:
            addresses = [
                ipaddress.ip_address(item[4][0])
                for item in socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80))
            ]
        except socket.gaierror as exc:
            raise ValueError("The URL hostname could not be resolved.") from exc
    if not addresses or any(
        not (addr.is_global and not addr.is_multicast and not addr.is_reserved)
        for addr in addresses
    ):
        raise ValueError("URLs resolving to private or reserved IP addresses are not allowed.")
    return url


def extract_text(html: str) -> str:
    """Convert HTML to readable text while dropping non-content elements."""
    soup = BeautifulSoup(html, "html.parser")
    for element in soup(["script", "style", "noscript", "svg", "nav", "footer", "header", "form"]):
        element.decompose()
    root = soup.find("main") or soup.find("article") or soup.body or soup
    return " ".join(root.get_text(separator=" ", strip=True).split())


def scrape_text(url: str, max_chars: int = 200_000) -> str:
    """Fetch a public HTML page with redirect, size, and timeout limits."""
    current = _validate_public_url(url)
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"}
    with requests.Session() as session:
        for redirect_count in range(MAX_REDIRECTS + 1):
            _validate_public_url(current)
            response = session.get(
                current, headers=headers, timeout=(5, 15), allow_redirects=False, stream=True
            )
            if response.is_redirect or response.is_permanent_redirect:
                location = response.headers.get("Location")
                response.close()
                if not location or redirect_count == MAX_REDIRECTS:
                    raise ValueError("The webpage redirected too many times.")
                current = urljoin(current, location)
                continue
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "").lower()
            if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
                response.close()
                raise ValueError("The URL did not return an HTML webpage.")
            length = response.headers.get("Content-Length")
            if length and int(length) > max_chars * 8:
                response.close()
                raise ValueError("The webpage is too large to ingest.")
            chunks = []
            total = 0
            for part in response.iter_content(chunk_size=16_384):
                total += len(part)
                if total > max_chars * 8:
                    response.close()
                    raise ValueError("The webpage is too large to ingest.")
                chunks.append(part)
            encoding = response.encoding or "utf-8"
            html = b"".join(chunks).decode(encoding, errors="replace")
            text = extract_text(html)[:max_chars]
            if len(text) < 40:
                raise ValueError("The webpage did not contain enough readable text.")
            return text
    raise ValueError("Could not fetch the webpage.")
