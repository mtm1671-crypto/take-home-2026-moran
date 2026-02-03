import type {Product} from "../types/product"
import { formatPrice } from "../utils/currency"

interface ProductCardProp {
    product: Product;
    onClick: () => void
}

export function ProductCard({product, onClick}: ProductCardProp){
    const currency = product.price.currency;
    const imageUrl = product.image_urls[0] || "";

    return (
        <div onClick={onClick} className = "cursor-pointer border rounded-lg p-4 hover:shadow-lg">
            {/*Image*/}
            {imageUrl ? (
                <img
                    src={imageUrl}
                    alt={product.name}
                    className="w-full h-48 object-cover"
                />
            ) : (
                <div className="w-full h-48 bg-gray-200 flex items-center justify-center text-gray-400">
                    No image
                </div>
            )}

            {/* brand */}
            <p className = "text-sm text-gray-500">{product.brand}</p>

            {/* Name */}
            <h3 className="font-medium truncate">{product.name}</h3>

            {/* Price */}
            <div>
                <span>{formatPrice(product.price.price, currency)}</span>
                {product.price.compare_at_price && (
                    <span className="line-through text-gray-300 ml-2">
                        {formatPrice(product.price.compare_at_price, currency)}
                    </span>
                )}
            </div>
        </div>
    );
}
