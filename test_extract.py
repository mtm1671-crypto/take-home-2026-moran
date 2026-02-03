
import pytest
import json
from preprocess import preprocess_html, extract_jsonld, extract_meta_tags, clean_html
from extract import clean_text, fix_url
from models import Product, Category, Price, Variant
from bs4 import BeautifulSoup


class TestPreprocessing:
    """Tests for HTML preprocessing functions."""

    def test_extract_jsonld_valid(self):
        """Should extract valid JSON-LD data from script tags."""
        html = '''
        <html>
            <script type="application/ld+json">
                {"@type": "Product", "name": "Test Product"}
            </script>
        </html>
        '''
        soup = BeautifulSoup(html, "html.parser")
        result = extract_jsonld(soup)
        assert len(result) == 1
        assert result[0]["@type"] == "Product"
        assert result[0]["name"] == "Test Product"

    def test_extract_jsonld_invalid_json(self):
        """Should skip invalid JSON without crashing."""
        html = '''
        <html>
            <script type="application/ld+json">
                {invalid json here}
            </script>
        </html>
        '''
        soup = BeautifulSoup(html, "html.parser")
        result = extract_jsonld(soup)
        assert len(result) == 0

    def test_extract_jsonld_empty(self):
        """Should return empty list when no JSON-LD present."""
        html = '<html><body>No JSON-LD here</body></html>'
        soup = BeautifulSoup(html, "html.parser")
        result = extract_jsonld(soup)
        assert result == []

    def test_extract_meta_tags(self):
        """Should extract meta tags and title."""
        html = '''
        <html>
            <head>
                <title>Product Page</title>
                <meta name="description" content="A great product">
                <meta property="og:title" content="OG Title">
            </head>
        </html>
        '''
        soup = BeautifulSoup(html, "html.parser")
        result = extract_meta_tags(soup)
        assert result["title"] == "Product Page"
        assert result["description"] == "A great product"
        assert result["og:title"] == "OG Title"

    def test_clean_html_removes_scripts(self):
        """Should remove script, style, and other non-content tags."""
        html = '''
        <html>
            <script>var x = 1;</script>
            <style>.foo { color: red; }</style>
            <body>
                <p>Visible content</p>
                <noscript>No JS fallback</noscript>
            </body>
        </html>
        '''
        soup = BeautifulSoup(html, "html.parser")
        result = clean_html(soup)
        assert "Visible content" in result
        assert "var x = 1" not in result
        assert "color: red" not in result
        assert "No JS fallback" not in result

    def test_preprocess_html_structure(self):
        """Should return structured output with JSON-LD, meta, and content."""
        html = '''
        <html>
            <head>
                <title>Test</title>
                <script type="application/ld+json">{"@type": "Product"}</script>
            </head>
            <body><p>Content here</p></body>
        </html>
        '''
        result = preprocess_html(html)
        assert "JSON-LD Data" in result
        assert "Meta Tags" in result
        assert "Page Content" in result
        assert "Content here" in result

    def test_preprocess_html_truncates_long_content(self):
        """Should truncate content over 10000 characters."""
        html = f'<html><body>{"x" * 15000}</body></html>'
        result = preprocess_html(html)
        assert "... [truncated]" in result


class TestTextCleaning:
    """Tests for text cleaning utilities."""

    def test_clean_text_normalizes_whitespace(self):
        """Should collapse multiple spaces and normalize newlines."""
        text = "Hello    world\r\n\r\ntest"
        result = clean_text(text)
        assert "Hello world" in result
        assert "\r" not in result

    def test_clean_text_removes_replacement_chars(self):
        """Should remove Unicode replacement characters."""
        text = "Hello � world \ufffd test"
        result = clean_text(text)
        assert "�" not in result
        assert "\ufffd" not in result

    def test_clean_text_handles_none(self):
        """Should handle None/empty input gracefully."""
        assert clean_text(None) is None
        assert clean_text("") == ""

    def test_fix_url_adds_https(self):
        """Should prepend https: to protocol-relative URLs."""
        assert fix_url("//example.com/image.jpg") == "https://example.com/image.jpg"
        assert fix_url("https://example.com/image.jpg") == "https://example.com/image.jpg"
        assert fix_url("http://example.com/image.jpg") == "http://example.com/image.jpg"

    def test_fix_url_handles_empty(self):
        """Should handle empty/None URLs."""
        assert fix_url("") == ""
        assert fix_url(None) is None


class TestModels:
    """Tests for Pydantic model validation."""

    def test_category_exact_match(self):
        """Should accept exact category matches."""
        cat = Category(name="Apparel & Accessories > Clothing > Pants")
        assert cat.name == "Apparel & Accessories > Clothing > Pants"

    def test_category_fuzzy_match(self):
        """Should fuzzy-match close category names."""
        # Slight typo should still match
        cat = Category(name="Apparel & Accessories > Clothing > Pant")
        assert cat.name == "Apparel & Accessories > Clothing > Pants"

    def test_category_invalid_raises(self):
        """Should raise error for completely invalid categories."""
        with pytest.raises(ValueError, match="not a valid category"):
            Category(name="Completely Invalid Category That Doesnt Exist")

    def test_price_model(self):
        """Should correctly parse price data."""
        price = Price(price=29.95, currency="USD", compare_at_price=39.95)
        assert price.price == 29.95
        assert price.currency == "USD"
        assert price.compare_at_price == 39.95

    def test_price_no_sale(self):
        """Should allow None for compare_at_price."""
        price = Price(price=29.95, currency="USD")
        assert price.compare_at_price is None

    def test_variant_model(self):
        """Should correctly parse variant data."""
        variant = Variant(size="M", sku="ABC123", color="Blue", aval=True)
        assert variant.size == "M"
        assert variant.sku == "ABC123"
        assert variant.color == "Blue"
        assert variant.aval is True

    def test_variant_defaults(self):
        """Should use defaults for optional variant fields."""
        variant = Variant()
        assert variant.size is None
        assert variant.sku is None
        assert variant.aval is True

    def test_product_model_complete(self):
        """Should correctly parse a complete product."""
        product = Product(
            name="Test Product",
            price=Price(price=99.99, currency="USD"),
            description="A test product",
            key_features=["Feature 1", "Feature 2"],
            image_urls=["https://example.com/img.jpg"],
            video_url=None,
            category=Category(name="Apparel & Accessories > Shoes"),
            brand="TestBrand",
            colors=["Red", "Blue"],
            variants=[Variant(size="M", color="Red")]
        )
        assert product.name == "Test Product"
        assert product.price.price == 99.99
        assert len(product.key_features) == 2
        assert len(product.variants) == 1


class TestIntegration:
    """Integration tests using real HTML samples."""

    def test_preprocess_reduces_tokens(self):
        """Preprocessing should significantly reduce token count."""
        # Simulate a typical product page
        html = f'''
        <html>
            <head>
                <script>{"x" * 10000}</script>
                <style>{"y" * 10000}</style>
                <script type="application/ld+json">{{"@type": "Product", "name": "Test"}}</script>
            </head>
            <body>
                <p>Product description here</p>
            </body>
        </html>
        '''
        raw_tokens = len(html) // 4
        processed = preprocess_html(html)
        processed_tokens = len(processed) // 4

        # Should achieve significant reduction
        reduction = (1 - processed_tokens / raw_tokens) * 100
        assert reduction > 50, f"Expected >50% reduction, got {reduction:.0f}%"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
