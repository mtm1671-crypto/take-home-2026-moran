import os
import ai
import asyncio
from models import Product
from prompts import extract_prompt
from preprocess import preprocess_html
import json

#this is going to be the function that extracts the product object. It borrows from prompts.py which is where we will customize the prompts
async def extract_product(html: str ) -> Product:
    # Preprocess HTML to reduce token usage (98% reduction!)
    processed = preprocess_html(html)

    return await ai.responses(
        #this is the choice due to the lightest option, which is important for scalablity
        model="google/gemini-2.0-flash-lite-001",
        input=[
            {"role": "system", "content": extract_prompt},
            {"role": "user", "content": processed}  # Use preprocessed instead of raw HTML
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

                product = await extract_product(html)
                products.append(product)
                print(f"success for {filename}")
                print(product.model_dump_json(indent=2))
            except Exception as e:
                print(f"fail on {filename}: {e}")
    with open("products.json","w") as f:
            json.dump([p.model_dump() for p in products], f, indent=2)
            #products to json

    print(f"\n--- Token Usage ---")
    print(f"Total tokens consumed: ~{total_tokens:,}")
    print(f"Estimated cost: ${total_tokens / 1_000_000 * 0.075:.4f}")
        
if __name__ == "__main__":
    asyncio.run(main())