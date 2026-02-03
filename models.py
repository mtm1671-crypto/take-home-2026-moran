from typing import Any
from pathlib import Path
from pydantic import BaseModel, field_validator
from difflib import get_close_matches
# Load categories once at module level
CATEGORIES_FILE = Path(__file__).parent / "categories.txt"
VALID_CATEGORIES = set()
if CATEGORIES_FILE.exists():
    with open(CATEGORIES_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                VALID_CATEGORIES.add(line)

class Category(BaseModel):
    # A category from Google's Product Taxonomy
    # https://www.google.com/basepages/producttype/taxonomy.en-US.txt
    name: str

    @field_validator("name")
    @classmethod
    def validate_name_exists(cls, v: str) -> str:
        if v in VALID_CATEGORIES:
            return v
        #this gets close matches betwween v and valid cats
        matches = get_close_matches(v,VALID_CATEGORIES, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        raise ValueError(f"Category '{v}' is not a valid category in categories.txt")

class Price(BaseModel):
    price: float
    currency: str
    # If a product is on sale, this is the original price
    compare_at_price: float | None = None

# This is the final product schema that you need to output. 
# You may add additional models as needed.
class Product(BaseModel):
    name: str
    price: Price
    description: str
    key_features: list[str]
    image_urls: list[str]
    video_url: str | None = None
    category: Category
    brand: str
    colors: list[str]
    variants: list["Variant"] # TODO (@dev): Define variant model
class Variant(BaseModel):
    size: str | None = None
    sku: str | None = None
    color: str | None = None
    price: Price | None = None
    aval: bool = True