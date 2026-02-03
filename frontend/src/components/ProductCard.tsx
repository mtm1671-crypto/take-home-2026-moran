import type {Product} from "../types/product"

interface ProductCardProp {
    product: Product;
    onClick: () => void
}

export function ProductCard({product, onClick}: ProductCardProp){
    return (
        <div onClick={onClick} className = "cursor-pointer border rounded-lg p-4 hover:shadow-lg">
            {/*Image*/}
            <img
                src={product.image_urls[0]}
                alt={product.name}
                className="w-full h-48 object-cover"
            />

            {/* brand */}
            <p className = "text-sm text-gray-500">{product.brand}</p>

            {/* Name */}
            <h3 className="font-medium truncate">{product.name}</h3>

            {/* Price */}
            <div>
                <span>${product.price.price}</span>
                {product.price.compare_at_price && (
                    <span className="line-through text-gray-300 ml-2">
                        ${product.price.compare_at_price}
                    </span>
                )}
            </div>
        </div>
    );
}