#hi channel team, this is the prompts storage, i find it useful
extract_prompt = """Extract product information from the provided HTML into the specified schema.

## Field Guidelines:

**name**: The product title/name as displayed on the page

**price**: 
- price: Current selling price as a float
- currency: ISO currency code (USD, GBP, EUR, etc.)
- compare_at_price: Original price if on sale, otherwise null

**description**: Full product description text

**key_features**: List of bullet points, specifications, or highlighted features

**image_urls**: ALL product image URLs at full resolution (not thumbnails). Look for:
- Main product images
- Alternate angle images
- Color variant images
- Zoom/high-res versions

**video_url**: Product video URL if available, otherwise null

**category**: MUST be an exact match from Google Product Taxonomy. Use full path with " > " separators.
Valid examples for reference:
- "Apparel & Accessories > Clothing > Pants"
- "Apparel & Accessories > Shoes"
- "Hardware > Tools > Drills > Handheld Power Drills"
- "Home & Garden > Lighting > Lamps"
- "Home & Garden > Decor > Rugs"
- "Furniture > Chairs"
- "Electronics > Electronics Accessories"
DO NOT invent categories. Use the most specific matching category that exists.

**brand**: The brand or manufacturer name

**colors**: List of available color options (e.g., ["Black", "Navy", "Iron"])

**variants**: All purchasable combinations. Each variant should include:
- sku: Product SKU/ID for this variant if available
- size: Size value (e.g., "M", "32x30", "One Size")
- color: Color name for this variant
- price: Price if different from main price, otherwise null
- aval: true if in stock, false if out of stock

## Data Sources:
Look for structured data first (JSON-LD, meta tags), then fall back to page content.
"""
