import type {Product} from "../types/product"

const currencySymbols: Record<string, string> = {
    USD: '$',
    GBP: '£',
    EUR: '€',
    JPY: '¥',
    CAD: 'C$',
    AUD: 'A$',
};

function formatPrice(amount: number, currency: string): string {
    const symbol = currencySymbols[currency] || currency + ' ';
    return `${symbol}${amount.toFixed(2)}`;
}

interface ProductCardProp {
    product: Product;
    onClick: () => void
}

export function ProductCard({product, onClick}: ProductCardProp){
    const currency = product.price.currency;

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