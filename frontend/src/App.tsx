import { useState } from 'react'
import type { Product } from './types/product'
import { ProductCard } from './components/ProductCard'
import { ProductDetail } from './components/ProductDetail'
import productsData from "./data/products.json"

console.log("Products loaded:", productsData);

function App(){
  const products = productsData as Product[]
  console.log("Rendering App with", products.length, "products");

  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  if(selectedProduct){
    return (
      <ProductDetail
        product= {selectedProduct}
        onBack={() => setSelectedProduct(null)}
      />
    );
  }
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Product Catalog</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* looooop */}
        {products.map((product,i) => (
          <ProductCard
            key={i}
            product={product}
            onClick={() => setSelectedProduct(product)}
            />
        ))}
      </div>
    </div>
  )
}
export default App;