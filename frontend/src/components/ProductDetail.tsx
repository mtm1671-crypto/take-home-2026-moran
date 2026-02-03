import type {Product} from "../types/product"

interface ProductDetailProps {
    product: Product;
    onBack: () => void;
}

export function ProductDetail({product, onBack}: ProductDetailProps){
    return (
        <div className ="max-w-4xl mx-auto p-4">
            {/* Back button */}
            <button onClick={onBack} className = "mb-4 text-blue-600">
                ← Back to catalog
            </button>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Left: Images! */}
                <div>
                    <img
                        src={product.image_urls[0]}
                        alt={product.name}
                        className="w-full rounded-lg"
                        />
                    {/* Thumbnail rows */}
                    <div className="flex gap-2 mt-2">
                        {product.image_urls.slice(0,4).map((url,i) => (
                            <img key = {i} src={url} className="w-16 h-16 object-cover rounded"/>
                            
                        ))}
                    </div>
                </div>
                {/* Right: Info */}
                <div>
                    <p className="text-sm text-gray-500">{product.brand}</p>
                    <h1 className="text-2xl font-bold">{product.name}</h1>
                
                {/* Price */}
                <div className="text-xl mt-2">
                    ${product.price.price}
                    {product.price.compare_at_price && (
                        <span className ="line-through text-gray-500 ml-2">
                            ${product.price.compare_at_price}
                        </span>
                    )}
                </div>
                {/*Colors */}
                {product.colors.length > 0 && (
                    <div className="mt-4">
                        <p className="font-medium">COLORS:</p>
                        <div className="flex gap-2 mt-1">
                            {product.colors.map((color) =>(
                                <span key={color} className="px-2 py-1 border rounded text-sm">
                                    {color}
                                </span>
                            ))}
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