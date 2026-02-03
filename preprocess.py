# HTML Preprocessor -
import json
from bs4 import BeautifulSoup
#gets the scripts
def extract_jsonld(soup: BeautifulSoup) -> list[dict]:
    jsonld_data = []
    
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            jsonld_data.append(data)
        except (json.JSONDecodeError, TypeError):
            continue
    return jsonld_data

#gets the meta tags
def extract_meta_tags(soup: BeautifulSoup) -> dict:

    
    meta_tags = {}
    for tag in soup.find_all("meta"):
        name = tag.get("name") or tag.get("property")
        content = tag.get("content")
        if name and content:
            meta_tags[name] = content
    title_tag = soup.find("title")
    if title_tag:
        meta_tags["title"] = title_tag.get_text(strip=True)
    return meta_tags
    

#cleans the rest of the html (accepts soup object to avoid re-parsing)
def clean_html(soup: BeautifulSoup) -> str:
    # Work on a copy to avoid modifying the original soup
    soup_copy = BeautifulSoup(str(soup), "html.parser")
    for tag in soup_copy.find_all(["script","style","noscript","iframe","svg"]):
        tag.decompose()
    text = soup_copy.get_text(separator="\n",strip=True)
    return text
#puts it all together + a bit of cleaning
def preprocess_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    jsonld = extract_jsonld(soup)
    meta = extract_meta_tags(soup)
    clean_text = clean_html(soup)

    if len(clean_text) > 10000:
        clean_text = clean_text[:10000] + "\n... [truncated]"
    parts = []
    
    if jsonld:
        parts.append("JSON-LD Data")
        parts.append(json.dumps(jsonld, indent=2))
    
    if meta:
        parts.append("\nMeta Tags")
        parts.append(json.dumps(meta, indent=2))
    
    parts.append("\nPage Content")
    parts.append(clean_text)
    
    #Join all parts into one string
    return "\n".join(parts)

#ai built test to see the difference
if __name__ == "__main__":
    import os

    # Rough estimate: 1 token ≈ 4 characters
    def estimate_tokens(text: str) -> int:
        return len(text) // 4

    # gemini-2.0-flash-lite pricing (per 1M tokens)
    INPUT_PRICE = 0.075  # $0.075 per 1M input tokens

    print("=" * 70)
    print(f"{'File':<20} {'Raw':>12} {'Processed':>12} {'Reduction':>10}")
    print("=" * 70)

    total_raw = 0
    total_processed = 0

    for filename in sorted(os.listdir("data")):
        if filename.endswith(".html"):
            with open(f"data/{filename}", "r", encoding="utf-8") as f:
                html = f.read()

            processed = preprocess_html(html)

            raw_tokens = estimate_tokens(html)
            proc_tokens = estimate_tokens(processed)
            reduction = (1 - proc_tokens / raw_tokens) * 100

            total_raw += raw_tokens
            total_processed += proc_tokens

            print(f"{filename:<20} {raw_tokens:>10,}t {proc_tokens:>10,}t {reduction:>9.0f}%")

    print("=" * 70)
    total_reduction = (1 - total_processed / total_raw) * 100
    print(f"{'TOTAL':<20} {total_raw:>10,}t {total_processed:>10,}t {total_reduction:>9.0f}%")

    avg_raw = total_raw / 5
    avg_proc = total_processed / 5

    print(f"\nCost at 50M products (gemini-2.0-flash-lite @ $0.075/1M tokens):")
    print(f"  Without preprocessing: ${avg_raw * 50_000_000 / 1_000_000 * INPUT_PRICE:,.0f}")
    print(f"  With preprocessing:    ${avg_proc * 50_000_000 / 1_000_000 * INPUT_PRICE:,.0f}")
    print(f"  SAVINGS:               ${(avg_raw - avg_proc) * 50_000_000 / 1_000_000 * INPUT_PRICE:,.0f}")
