import React from "react";

//Methods
import { getProductList } from "../../services/Product";

//Components
import ProductCard from "../../components/ui/cards/ProductCard/ProductCard";
import { Typography } from "@mui/material";
import { Button } from "@mui/material";
const DEMO_PRODUCTS = [
  {
    id: 1,
    slug: "classic-white-sneakers",
    product_type: "Shoes",
    product_name: "Classic White Sneakers",
    price: 89.99,
    sale_price: 69.99,
    blurb: "Timeless, comfortable everyday footwear.",
    image_url: "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&auto=format&fit=crop&q=60"
  },
  {
    id: 2,
    slug: "casual-denim-jacket",
    product_type: "Tops",
    product_name: "Casual Denim Jacket",
    price: 119.00,
    sale_price: 99.00,
    blurb: "Rugged vintage wash denim jacket.",
    image_url: "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=500&auto=format&fit=crop&q=60"
  },
  {
    id: 3,
    slug: "slim-fit-chinos",
    product_type: "Bottoms",
    product_name: "Slim Fit Stretch Chinos",
    price: 59.50,
    sale_price: null,
    blurb: "Versatile smart-casual trousers.",
    image_url: "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500&auto=format&fit=crop&q=60"
  },
  {
    id: 4,
    slug: "minimalist-leather-watch",
    product_type: "Accessories",
    product_name: "Minimalist Leather Watch",
    price: 149.00,
    sale_price: 129.00,
    blurb: "Clean aesthetic with genuine leather strap.",
    image_url: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60"
  }
];

export default function Products() {
  const [products, setProducts] = React.useState<any[]>([]);
  const [loading, setLoading] = React.useState<boolean>(true);
  const [isDemoData, setIsDemoData] = React.useState<boolean>(false);

  React.useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await getProductList({ page: 0, limit: 10 });
        if (response && Array.isArray(response) && response.length > 0) {
          setProducts(response);
          setIsDemoData(false);
        } else {
          // Fallback to sample demo products if database has no items yet
          setProducts(DEMO_PRODUCTS);
          setIsDemoData(true);
        }
      } catch (err) {
        setProducts(DEMO_PRODUCTS);
        setIsDemoData(true);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <main className="p-6">
      <section id="filters" className="flex gap-4 mb-4 justify-start">
        <Button variant="outlined">Fit</Button>
        <Button variant="outlined">Color</Button>
        <Button variant="outlined">Price</Button>
      </section>

      {isDemoData && (
        <div className="mb-6 p-3 bg-blue-50 border border-blue-200 text-blue-800 text-sm rounded text-left">
          Showing <strong>preview sample products</strong>. Connect your PostgreSQL database and run <code className="bg-blue-100 px-1 py-0.5 rounded">python seed.py</code> in the backend to serve dynamic data.
        </div>
      )}

      <section
        id="product-info"
        className="flex flex-wrap gap-[2rem] justify-start"
      >
        {loading ? (
          <div className="text-gray-500 py-12 w-full text-center">Loading products...</div>
        ) : (
          <>
            {products && products.length > 0 ? (
              products.map((product, i) => (
                <ProductCard key={product.id || product.slug || i} product={product} />
              ))
            ) : (
              <div className="text-center py-16 text-gray-500 w-full">
                <p className="text-xl font-semibold mb-2">No products available yet</p>
                <p className="text-sm">Once the backend database is connected and products are added, they will appear here.</p>
              </div>
            )}
          </>
        )}
      </section>
    </main>
  );
}
