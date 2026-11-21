import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.services.product_service import Product_Service
from app.models.sqlalchemy.product import Product

def test_product_service_get_products_with_session():
    """Verify that Product_Service.get_products executes query on provided session."""
    mock_db = MagicMock(spec=Session)
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = []

    result = Product_Service.get_products(mock_db, page=1, limit=10)
    assert result == []
    mock_db.query.assert_called_once_with(Product)
    mock_query.offset.assert_called_once_with(10)
    mock_query.limit.assert_called_once_with(10)

def test_product_service_get_product_with_session():
    """Verify that Product_Service.get_product queries by slug using provided session."""
    mock_db = MagicMock(spec=Session)
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    
    mock_product = Product(
        id=1,
        slug="test-item",
        product_name="Test Item",
        product_type="Shoes",
        price=99.0,
        sale_price=None,
        blurb="Blurb",
        description="Desc",
        image_url=None
    )
    mock_query.one.return_value = mock_product

    result = Product_Service.get_product(mock_db, product_slug="test-item")
    assert result.slug == "test-item"
    mock_db.query.assert_called_once_with(Product)

def test_product_service_update_product_with_session():
    """Verify that Product_Service.update_product updates attributes using provided session."""
    mock_db = MagicMock(spec=Session)
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    
    mock_product = Product(
        id=1,
        slug="test-item",
        product_name="Old Name",
        product_type="Shoes",
        price=99.0,
        sale_price=None,
        blurb="Blurb",
        description="Desc",
        image_url=None
    )
    mock_product.categories = []
    mock_product.sizes = []
    mock_query.first.return_value = mock_product

    mock_update_schema = MagicMock()
    mock_update_schema.dict.return_value = {"product_name": "New Name"}

    result = Product_Service.update_product(mock_db, "test-item", mock_update_schema)
    assert mock_product.product_name == "New Name"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_product)

def test_product_service_delete_product_with_session():
    """Verify that Product_Service.delete_product deletes record using provided session."""
    mock_db = MagicMock(spec=Session)
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    
    mock_product = Product(id=1, slug="delete-me")
    mock_query.first.return_value = mock_product

    success = Product_Service.delete_product(mock_db, "delete-me")
    assert success is True
    mock_db.delete.assert_called_once_with(mock_product)
    mock_db.commit.assert_called_once()

def test_product_service_delete_nonexistent_product():
    """Verify delete_product returns False when product is not found."""
    mock_db = MagicMock(spec=Session)
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None

    success = Product_Service.delete_product(mock_db, "nonexistent")
    assert success is False
    mock_db.delete.assert_not_called()
