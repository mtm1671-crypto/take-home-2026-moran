import ai
import asyncio
import logging
from pydantic import BaseModel

async def hello_world():
    class HelloWorldResponse(BaseModel):
        message: str
    response = await ai.responses(
        "gpt-5-nano",
        [{"role": "system", "content": "You are a helpful assistant that outputs everything in reverse."},
         {"role": "user", "content": "Say 'hello world'"}],
        text_format=HelloWorldResponse)
    logging.info(response.message)

if __name__ == "__main__":
    import os
    
    # Rough estimate: 1 token ≈ 4 characters
    def estimate_tokens(text: str) -> int:
        return len(text) // 4
    
    # gemini-2.0-flash-lite pricing (per 1M tokens)
    INPUT_PRICE = 0.075  # $0.075 per 1M input tokens
    
    print("=" * 70)
    print(f"{'File':<20} {'Raw':>12} {'Processed':>12} {'Reduction':>10} {'Cost/1M':>12}")
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
            
            # Cost to process 1 million products
            raw_cost = (raw_tokens * 1_000_000 / 1_000_000) * INPUT_PRICE
            proc_cost = (proc_tokens * 1_000_000 / 1_000_000) * INPUT_PRICE
            
            total_raw += raw_tokens
            total_processed += proc_tokens
            
            print(f"{filename:<20} {raw_tokens:>10,}t {proc_tokens:>10,}t {reduction:>9.0f}% ${proc_cost:>10,.0f}")
    
    print("=" * 70)
    total_reduction = (1 - total_processed / total_raw) * 100
    print(f"{'TOTAL':<20} {total_raw:>10,}t {total_processed:>10,}t {total_reduction:>9.0f}%")
    print(f"\nAt 50M products:")
    print(f"  Without preprocessing: ${total_raw / 5 * 50_000_000 / 1_000_000 * INPUT_PRICE:,.0f}")
    print(f"  With preprocessing:    ${total_processed / 5 * 50_000_000 / 1_000_000 * INPUT_PRICE:,.0f}")

