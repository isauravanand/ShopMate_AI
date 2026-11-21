import os
from dotenv import load_dotenv

load_dotenv()

from app.db import get_db_session, create_tables
from app.models.sqlalchemy.product import Product, ProductSize
from app.models.sqlalchemy.category import Category

CATEGORIES = [
    {"name": "New Arrivals", "description": "The latest styles and trends just dropped."},
    {"name": "Tops", "description": "T-shirts, hoodies, jackets, and shirts."},
    {"name": "Bottoms", "description": "Chinos, jeans, pants, and shorts."},
    {"name": "Shoes", "description": "Sneakers, boots, and casual footwear."},
    {"name": "Accessories", "description": "Watches, bags, sunglasses, and belts."},
    {"name": "Sale", "description": "Discounted styles and promotional offers."}
]

REAL_PRODUCTS = [
    # --- SHOES ---
    {
        "slug": "classic-white-sneakers",
        "product_type": "Shoes",
        "product_name": "Urban Low-Top Leather Sneakers",
        "price": 89.99,
        "sale_price": 69.99,
        "blurb": "Clean, versatile white leather sneakers engineered for all-day comfort.",
        "description": "Crafted from supple full-grain calfskin with an orthotic arch support insole and durable vulcanized rubber cupsole. Perfect for casual wear, office attire, or city walking.",
        "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=700&auto=format&fit=crop&q=80",
        "categories": ["Shoes", "New Arrivals", "Sale"],
        "sizes": [("8", 25), ("9", 35), ("10", 40), ("11", 20)]
    },
    {
        "slug": "retro-runner-trainers",
        "product_type": "Shoes",
        "product_name": "Retro Colorblock Trail Runners",
        "price": 125.00,
        "sale_price": 99.00,
        "blurb": "Vintage 90s aesthetic meets modern responsive cushioning.",
        "description": "Layered suede and breathable mesh upper with high-traction waffle rubber outsole. Responsive EVA foam midsole provides lightweight energy return.",
        "image_url": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=700&auto=format&fit=crop&q=80",
        "categories": ["Shoes", "Sale"],
        "sizes": [("8.5", 15), ("9.5", 30), ("10.5", 25), ("11.5", 10)]
    },
    {
        "slug": "leather-chelsea-boots",
        "product_type": "Shoes",
        "product_name": "Heritage Chelsea Boots in Amber",
        "price": 185.00,
        "sale_price": None,
        "blurb": "Hand-burnished leather boots with elasticated side gussets.",
        "description": "Handcrafted in Portugal using vegetable-tanned bovine leather with Goodyear-welted rubber lug soles. Gets better with age and develops a rich natural patina.",
        "image_url": "https://images.unsplash.com/photo-1638247025967-b4e38f787b76?w=700&auto=format&fit=crop&q=80",
        "categories": ["Shoes", "New Arrivals"],
        "sizes": [("8", 12), ("9", 18), ("10", 22), ("11", 14)]
    },
    {
        "slug": "canvas-high-tops",
        "product_type": "Shoes",
        "product_name": "Monochrome Canvas High-Tops",
        "price": 65.00,
        "sale_price": 49.99,
        "blurb": "Timeless skate-inspired silhouette with reinforced toe cap.",
        "description": "Heavyweight 12oz organic cotton canvas upper with nickel eyelets, padded collar, and vulcanized rubber traction waffle outsole.",
        "image_url": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=700&auto=format&fit=crop&q=80",
        "categories": ["Shoes", "Sale"],
        "sizes": [("7", 10), ("8", 20), ("9", 30), ("10", 25)]
    },

    # --- TOPS ---
    {
        "slug": "oversized-heavyweight-hoodie",
        "product_type": "Tops",
        "product_name": "Heavyweight French Terry Hoodie",
        "price": 95.00,
        "sale_price": 79.00,
        "blurb": "450 GSM ultra-dense combed cotton with double-lined hood.",
        "description": "Pre-shrunk custom-milled loopback French terry fleece. Features dropped shoulders, ribbed side gussets, kangaroo pocket, and lint-free interior.",
        "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=700&auto=format&fit=crop&q=80",
        "categories": ["Tops", "New Arrivals", "Sale"],
        "sizes": [("S", 20), ("M", 45), ("L", 50), ("XL", 25)]
    },
    {
        "slug": "vintage-denim-trucker-jacket",
        "product_type": "Tops",
        "product_name": "Vintage Wash Denim Trucker Jacket",
        "price": 139.00,
        "sale_price": 109.00,
        "blurb": "Classic 13.5oz denim with distressed wash detailing.",
        "description": "100% selvedge cotton denim with antique brass buttons, dual chest pockets, and waist adjusters. Timeless layering staple.",
        "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=700&auto=format&fit=crop&q=80",
        "categories": ["Tops", "Sale"],
        "sizes": [("S", 15), ("M", 30), ("L", 35), ("XL", 15)]
    },
    {
        "slug": "oxford-cotton-button-down",
        "product_type": "Tops",
        "product_name": "Tailored Oxford Cloth Button-Down",
        "price": 78.00,
        "sale_price": None,
        "blurb": "Smart everyday shirt in breathable basketweave cotton.",
        "description": "Subtle tailored fit with a classic button-down collar, box pleat for mobility, and durable genuine horn buttons. Washed for instant softness.",
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=700&auto=format&fit=crop&q=80",
        "categories": ["Tops", "New Arrivals"],
        "sizes": [("S", 18), ("M", 40), ("L", 40), ("XL", 20)]
    },
    {
        "slug": "minimalist-pima-tee",
        "product_type": "Tops",
        "product_name": "Premium Supima Crewneck T-Shirt",
        "price": 38.00,
        "sale_price": 28.00,
        "blurb": "Silky-smooth extra-long staple Supima cotton tee.",
        "description": "Featherlight yet durable combed cotton with ribbed collar and blind stitch hem. Designed to never lose shape or pill after washing.",
        "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=700&auto=format&fit=crop&q=80",
        "categories": ["Tops", "Sale"],
        "sizes": [("XS", 10), ("S", 30), ("M", 50), ("L", 50), ("XL", 30)]
    },
    {
        "slug": "chunky-knit-merino-sweater",
        "product_type": "Tops",
        "product_name": "Ribbed Merino Wool Crewneck",
        "price": 145.00,
        "sale_price": None,
        "blurb": "100% fine Australian Merino wool with thermal knit texture.",
        "description": "Naturally temperature-regulating, itch-free, and odor-resistant. Features saddle shoulder seams and reinforced ribbed trims.",
        "image_url": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=700&auto=format&fit=crop&q=80",
        "categories": ["Tops", "New Arrivals"],
        "sizes": [("S", 15), ("M", 25), ("L", 25), ("XL", 12)]
    },

    # --- BOTTOMS ---
    {
        "slug": "slim-fit-stretch-chinos",
        "product_type": "Bottoms",
        "product_name": "Everyday Slim Stretch Chino",
        "price": 68.00,
        "sale_price": 54.00,
        "blurb": "Work-to-weekend comfort with 4-way stretch twill fabric.",
        "description": "97% cotton and 3% elastane for maximum range of motion. Features slanted front pockets, welt back pockets with button closures, and reinforced crotch gusset.",
        "image_url": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=700&auto=format&fit=crop&q=80",
        "categories": ["Bottoms", "Sale"],
        "sizes": [("30", 20), ("32", 40), ("34", 40), ("36", 20)]
    },
    {
        "slug": "relaxed-selvedge-denim",
        "product_type": "Bottoms",
        "product_name": "Japanese Raw Selvedge Jeans",
        "price": 165.00,
        "sale_price": None,
        "blurb": "14oz shuttle-loomed Kaihara denim with red selvedge ID.",
        "description": "Authentic mid-rise, straight leg fit made with 100% ring-spun indigo cotton. Unwashed raw denim ready for personalized fading over time.",
        "image_url": "https://images.unsplash.com/photo-1542272604-780c96856592?w=700&auto=format&fit=crop&q=80",
        "categories": ["Bottoms", "New Arrivals"],
        "sizes": [("30", 15), ("32", 30), ("34", 30), ("36", 15)]
    },
    {
        "slug": "tactical-cargo-trousers",
        "product_type": "Bottoms",
        "product_name": "Utility Modular Cargo Pants",
        "price": 110.00,
        "sale_price": 88.00,
        "blurb": "Ripstop cotton cargos with magnetic flap utility pockets.",
        "description": "Reinforced knees, adjustable drawcord cuffs, water-repellent DWR coating, and 6 secure pockets designed for outdoor exploration and modern streetwear.",
        "image_url": "https://images.unsplash.com/photo-1517445312882-bc9910d016b7?w=700&auto=format&fit=crop&q=80",
        "categories": ["Bottoms", "Sale"],
        "sizes": [("S", 15), ("M", 35), ("L", 35), ("XL", 15)]
    },

    # --- ACCESSORIES ---
    {
        "slug": "minimalist-leather-watch",
        "product_type": "Accessories",
        "product_name": "Chronograph 40mm Quartz Watch",
        "price": 179.00,
        "sale_price": 139.00,
        "blurb": "Clean Bauhaus aesthetic with vegetable-tanned leather strap.",
        "description": "Brushed 316L stainless steel casing, scratch-resistant sapphire crystal glass, 5 ATM water resistance, and accurate Japanese Miyota movement.",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=700&auto=format&fit=crop&q=80",
        "categories": ["Accessories", "New Arrivals", "Sale"],
        "sizes": [("One Size", 50)]
    },
    {
        "slug": "waterproof-commuter-backpack",
        "product_type": "Accessories",
        "product_name": "Modular City Commuter Backpack 24L",
        "price": 135.00,
        "sale_price": None,
        "blurb": "Weatherproof matte coated canvas with dedicated 16\" laptop sleeve.",
        "description": "Ergonomic mesh back padding, luggage passthrough strap, hidden passport pocket, magnetic Fidlock buckle, and YKK Aquaguard water-resistant zippers.",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=700&auto=format&fit=crop&q=80",
        "categories": ["Accessories", "New Arrivals"],
        "sizes": [("24L", 35)]
    },
    {
        "slug": "polarized-acetate-sunglasses",
        "product_type": "Accessories",
        "product_name": "Tortoiseshell Polarized Sunglasses",
        "price": 115.00,
        "sale_price": 89.00,
        "blurb": "Handmade Italian acetate frames with 100% UV400 polarized lenses.",
        "description": "5-barrel OBE hinges for lifetime durability, anti-reflective interior coating, and glare-reduction technology. Includes hard leather carry case.",
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=700&auto=format&fit=crop&q=80",
        "categories": ["Accessories", "Sale"],
        "sizes": [("Standard", 40)]
    },
    {
        "slug": "leather-bifold-wallet",
        "product_type": "Accessories",
        "product_name": "RFID-Blocking Slim Leather Wallet",
        "price": 55.00,
        "sale_price": 39.00,
        "blurb": "Top-grain cowhide bifold holding up to 10 cards and cash.",
        "description": "Ultra-slim profile engineered with embedded RFID shielding mesh to protect against wireless card skimming. Hand-stitched with waxed thread.",
        "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=700&auto=format&fit=crop&q=80",
        "categories": ["Accessories", "Sale"],
        "sizes": [("One Size", 60)]
    }
]

def seed_full_catalog():
    create_tables()
    session = get_db_session()
    if session is None:
        print("Database connection could not be established.")
        return

    try:
        # 1. Clear existing seed products and categories for clean refresh
        print("Refreshing product catalog...")
        session.query(ProductSize).delete()
        session.query(Product).delete()
        session.query(Category).delete()
        session.commit()

        # 2. Seed Categories
        category_map = {}
        for cat_data in CATEGORIES:
            category = Category(name=cat_data["name"], description=cat_data["description"])
            session.add(category)
            category_map[cat_data["name"]] = category
        session.commit()
        print(f"Created {len(category_map)} categories.")

        # 3. Seed Products with Categories and Sizes
        for prod_data in REAL_PRODUCTS:
            product = Product(
                slug=prod_data["slug"],
                product_type=prod_data["product_type"],
                product_name=prod_data["product_name"],
                price=prod_data["price"],
                sale_price=prod_data.get("sale_price"),
                blurb=prod_data.get("blurb"),
                description=prod_data.get("description"),
                image_url=prod_data.get("image_url")
            )

            # Associate categories
            for cat_name in prod_data.get("categories", []):
                if cat_name in category_map:
                    product.categories.append(category_map[cat_name])

            session.add(product)
            session.flush()

            # Associate sizes
            for size_name, qty in prod_data.get("sizes", []):
                ps = ProductSize(
                    product_id=product.id,
                    size=size_name,
                    stock_quantity=qty
                )
                session.add(ps)

        session.commit()
        print(f"Successfully seeded {len(REAL_PRODUCTS)} high-quality real products with sizes and categories!")

    except Exception as e:
        session.rollback()
        print(f"Error during catalog seeding: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_full_catalog()
