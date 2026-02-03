import os
import ai
import asyncio
import re
from models import Product
from prompts import extract_prompt
from preprocess import preprocess_html
import json
#ai built function to make sure the text we are extracting looks prettier
def clean_text(text: str) -> str:
    if not text:
        return text
    # Remove replacement characters and other junk
    text = text.replace('�', '').replace('\ufffd', '')
    # Normalize line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Collapse tabs and multiple spaces into single space
    text = re.sub(r'[\t ]+', ' ', text)
    # Clean up space around newlines
    text = re.sub(r' *\n *', '\n', text)
    # Collapse multiple newlines into max two
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove leading dash-space patterns that got mangled
    text = re.sub(r'^- +', '- ', text, flags=re.MULTILINE)
    return text.strip()

def fix_url(url: str) -> str:
    if url and url.startswith('//'):
        return 'https:' + url
    return url

#this is going to be the function that extracts the product object. It borrows from prompts.py which is where we will customize the prompts
async def extract_product(processed: str) -> Product:
    return await ai.responses(
        #this is the choice due to the lightest option, which is important for scalablity
        model="google/gemini-2.0-flash-lite-001",
        input=[
            {"role": "system", "content": extract_prompt},
            {"role": "user", "content": processed}
        ],
        text_format=Product
    )
#This is going to be the loop that actually get the products from the pages
async def main():
    data_folder = "data"
    products = []
    total_tokens = 0

    # rough estimate: 1 token ≈ 4 characters
    def estimate_tokens(text: str) -> int:
        return len(text) // 4

    #the loop of html files
    for filename in os.listdir(data_folder):
        if filename.endswith(".html"):
            filepath = os.path.join(data_folder,filename)
            with open(filepath, "r",encoding ="utf-8") as f:
                html = f.read()
            #try catch block so it can actually skip over errors
            try:
                processed = preprocess_html(html)
                tokens_used = estimate_tokens(processed)
                total_tokens += tokens_used

                product = await extract_product(processed)
                # clean up whitespace garbage from text fields
                product.description = clean_text(product.description)
                product.key_features = [clean_text(f) for f in product.key_features]
                # fix protocol-relative URLs
                product.image_urls = [fix_url(u) for u in product.image_urls]
                if product.video_url:
                    product.video_url = fix_url(product.video_url)
                products.append(product)
                print(f"success for {filename}")
                print(product.model_dump_json(indent=2))
            except Exception as e:
                print(f"fail on {filename}: {e}")
    # Write to root for backend use
    output_data = [p.model_dump() for p in products]
    with open("products.json", "w") as f:
        json.dump(output_data, f, indent=2)

    # Also write to frontend for UI (single pipeline)
    frontend_path = os.path.join("frontend", "src", "data", "products.json")
    os.makedirs(os.path.dirname(frontend_path), exist_ok=True)
    with open(frontend_path, "w") as f:
        json.dump(output_data, f, indent=2)
    print(f"Wrote {len(products)} products to products.json and {frontend_path}")

    print(f"\n--- Token Usage ---")
    print(f"Total tokens consumed: ~{total_tokens:,}")
    print(f"Estimated cost: ${total_tokens / 1_000_000 * 0.075:.4f}")
        
if __name__ == "__main__":
    asyncio.run(main())