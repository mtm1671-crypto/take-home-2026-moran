import { useState } from "react";
import type {Product} from "../types/product"
import { formatPrice } from "../utils/currency"

interface ProductDetailProps {
    product: Product;
    onBack: () => void;
}

export function ProductDetail({product, onBack}: ProductDetailProps){
    const [selectedImage, setSelectedImage] = useState(0);
    const [selectedVariant, setSelectedVariant] = useState<number | null>(null);

    // Get unique sizes from variants (filter out null sizes)
    const sizes = product.variants
        .filter(v => v.size !== null)
        .map(v => v.size as string);
    const uniqueSizes = [...new Set(sizes)];

    const currency = product.price.currency;
    const hasImages = product.image_urls.length > 0;
    const currentImage = hasImages ? product.image_urls[selectedImage] : "";

    return (
        <div className ="max-w-4xl mx-auto p-4">
            {/* Back button */}
            <button onClick={onBack} className = "mb-4 text-blue-600">
                ← Back to catalog
            </button>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Left: Images! */}
                <div>
                    {hasImages ? (
                        <img
                            src={currentImage}
                            alt={product.name}
                            className="w-full rounded-lg"
                        />
                    ) : (
                        <div className="w-full h-64 bg-gray-200 rounded-lg flex items-center justify-center text-gray-400">
                            No image available
                        </div>
                    )}
                    {/* Thumbnail rows */}
                    {product.image_urls.length > 1 && (
                        <div className="flex gap-2 mt-2">
                            {product.image_urls.slice(0,4).map((url,i) => (
                                <img
                                    key={i}
                                    src={url}
                                    onClick={() => setSelectedImage(i)}
                                    className={`w-16 h-16 object-cover rounded cursor-pointer border-2 ${
                                        selectedImage === i ? 'border-blue-500' : 'border-transparent'
                                    }`}
                                />
                            ))}
                        </div>
                    )}
                </div>
                {/* Right: Info */}
                <div>
                    <p className="text-sm text-gray-500">{product.brand}</p>
                    <h1 className="text-2xl font-bold">{product.name}</h1>

                {/* Price */}
                <div className="text-xl mt-2">
                    {formatPrice(product.price.price, currency)}
                    {product.price.compare_at_price && (
                        <span className ="line-through text-gray-500 ml-2">
                            {formatPrice(product.price.compare_at_price, currency)}
                        </span>
                    )}
                </div>
                {/*Colors */}
                {product.colors.length > 0 && (
                    <div className="mt-4">
                        <p className="font-medium">COLOR:</p>
                        <div className="flex gap-2 mt-1">
                            {product.colors.map((color) =>(
                                <span key={color} className="px-2 py-1 border rounded text-sm">
                                    {color}
                                </span>
                            ))}
                        </div>
                    </div>
                )}
                {/* Size selector */}
                {uniqueSizes.length > 0 && (
                    <div className="mt-4">
                        <p className="font-medium">SIZE:</p>
                        <div className="flex flex-wrap gap-2 mt-1">
                            {uniqueSizes.map((size, i) => {
                                const variant = product.variants.find(v => v.size === size);
                                const isAvailable = variant?.aval !== false;
                                return (
                                    <button
                                        key={size}
                                        onClick={() => setSelectedVariant(i)}
                                        disabled={!isAvailable}
                                        className={`px-3 py-2 border rounded text-sm ${
                                            selectedVariant === i
                                                ? 'border-blue-500 bg-blue-50'
                                                : isAvailable
                                                    ? 'hover:border-gray-400'
                                                    : 'opacity-40 cursor-not-allowed line-through'
                                        }`}
                                    >
                                        {size}
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                )}
                {/* Description */}
                <p className="mt-4 text-gray-600">{product.description}</p>
                {/*Features*/}
                {product.key_features.length > 0 && (
                    <ul className="mt-4 list-disc list-inside">
                        {product.key_features.map((feature,i) =>(
                            <li key={i}>{feature}</li>
                        ))}
                    </ul>
                )}
                </div>
            </div>
        </div>
    );
}
