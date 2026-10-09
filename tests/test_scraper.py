import pytest

from scraper import _validate_public_url, extract_text


def test_extract_text_removes_navigation_and_scripts():
    html = """<html><body><nav>menu</nav><main><h1>Useful heading</h1><p>Useful article text.</p><script>secret()</script><footer>footer links</footer></main></body></html>"""
    result = extract_text(html)
    assert "Useful heading" in result
    assert "Useful article text." in result
    assert "secret()" not in result
    assert "footer links" not in result
    assert "menu" not in result


@pytest.mark.parametrize("url", [
    "file:///etc/passwd", "ftp://example.com/file", "http://localhost/admin",
    "http://127.0.0.1/", "http://192.168.1.10/",
])
def test_validate_public_url_rejects_unsafe_urls(url):
    with pytest.raises(ValueError):
        _validate_public_url(url)
