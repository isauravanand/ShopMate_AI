from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.sqlalchemy import Product, ProductSize, Category
from app.schemas.product_schemas import ProductBase, ProductResponse, CategoryResponse, ProductSizeResponse
from fastapi import HTTPException
from fastapi_pagination import Page, paginate
import os
from colorama import Fore

from datetime import datetime

def map_product_to_response(db_product: Product) -> ProductResponse:
    categories = [CategoryResponse(name=category.name, id=category.id) for category in db_product.categories]
    sizes = [ProductSizeResponse(size=size.size, stock_quantity=size.stock_quantity, size_id=size.size_id) for size in db_product.sizes]
    return ProductResponse(
        id=db_product.id,
        slug=db_product.slug,
        product_type=db_product.product_type,
        product_name=db_product.product_name,
        price=db_product.price,
        blurb=db_product.blurb,
        description=db_product.description,
        image_url=db_product.image_url,
        categories=categories,
        sizes=sizes,
        sale_price=db_product.sale_price,
        created_at=getattr(db_product, 'created_at', None) or datetime.utcnow()
    )
class Product_Service():
    
    # Create a new product
    @staticmethod
    def create_product(db: Session, product: ProductBase) -> Dict:
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return map_product_to_response(db_product).dict()

    # Get a list of all products
    @staticmethod
    def get_products(db: Session, page: int = 0, limit: int = 10) -> List[Dict]:
        try:
            products = db.query(Product).offset(page * limit).limit(10).all()
            return products
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error fetching products")

    # Get a single product by ID
    @staticmethod
    def get_product(db: Session, product_slug: str):
        try:
            product = db.query(Product).filter(Product.slug == product_slug).one()
            return product
        except Exception as e:
            db.rollback()  # Ensure to rollback on any error.
            raise HTTPException(status_code=404, detail="Product not found")

    # Update a product
    @staticmethod
    def update_product(db: Session, product_slug: str, product: ProductBase) -> Dict:
        db_product = db.query(Product).filter(Product.slug == product_slug).first()
        if db_product:
            update_data = product.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_product, key, value)
            db.commit()
            db.refresh(db_product)
            return map_product_to_response(db_product).dict()
        return {}

    # Delete a product
    @staticmethod
    def delete_product(db: Session, product_slug: str) -> bool:
        db_product = db.query(Product).filter(Product.slug == product_slug).first()
        if db_product:
            db.delete(db_product)
            db.commit()
            return True
        return False

