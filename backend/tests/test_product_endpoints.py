import pytest
from fastapi.testclient import TestClient
from app.app import app
from app.db import get_db
from app.models.sqlalchemy.product import Product

@pytest.fixture
def client():
    return TestClient(app)

def test_product_listing_endpoint_status_and_structure(client):
    """Verify that GET /products returns HTTP 200 and a list of products using injected session."""
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        first_product = data[0]
        assert "slug" in first_product
        assert "product_name" in first_product
        assert "price" in first_product

def test_product_detail_endpoint_valid_slug(client):
    """Verify that GET /products/{product_slug} returns HTTP 200 for an existing product."""
    # First get a valid product slug from listing
    list_response = client.get("/products")
    assert list_response.status_code == 200
    products = list_response.json()
    
    if len(products) > 0:
        test_slug = products[0]["slug"]
        detail_response = client.get(f"/products/{test_slug}")
        assert detail_response.status_code == 200
        product_data = detail_response.json()
        assert product_data["slug"] == test_slug
        assert "product_name" in product_data
        assert "price" in product_data

def test_product_detail_endpoint_nonexistent_slug(client):
    """Verify that GET /products/{slug} returns HTTP 404 when product is not found."""
    response = client.get("/products/non-existent-sample-slug-99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_dependency_override_isolation(client):
    """Verify that FastAPI dependency_overrides[get_db] allows isolated mocking of database session."""
    from unittest.mock import MagicMock
    from sqlalchemy.orm import Session
    from app.models.sqlalchemy.product import Product

    mock_session = MagicMock(spec=Session)
    mock_product = Product(
        id=999,
        slug="mocked-test-product",
        product_name="Mocked Test Product",
        product_type="Test",
        price=49.99,
        sale_price=None,
        blurb="Test blurb",
        description="Test description",
        image_url=None
    )

    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [mock_product]

    def override_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["slug"] == "mocked-test-product"
        mock_session.query.assert_called_once()
    finally:
        app.dependency_overrides.clear()
