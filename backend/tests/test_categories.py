import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from app.models.category import Category
from app.models.product import Product


def test_create_and_read_category(db_session):
    category = Category(
        name="Кераміка",
        slug="ceramics",
        position=1,
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    saved_category = db_session.query(Category).filter_by(slug="ceramics").first()
    assert saved_category is not None
    assert saved_category.name == "Кераміка"
    assert saved_category.is_visible is False


def test_category_slug_unique_constraint(db_session):
    cat1 = Category(name="Категорія 1", slug="test-slug", position=1)
    db_session.add(cat1)
    db_session.commit()

    cat2 = Category(name="Категорія 2", slug="test-slug", position=2)
    db_session.add(cat2)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_get_public_categories_empty(client: TestClient):
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert response.json() == []


def test_get_public_categories_filtering_ordering_and_product_count(client: TestClient, db_session):
    cat_second = Category(
        name="Текстиль",
        slug="tekstyl",
        position=2,
        is_visible=True,
    )
    cat_first = Category(
        name="Кераміка",
        slug="keramika",
        position=1,
        is_visible=True,
        image_path="categories/keramika.jpg",
    )
    cat_hidden = Category(
        name="Прикраси",
        slug="prykrasy",
        position=0,
        is_visible=False,
    )
    db_session.add_all([cat_second, cat_first, cat_hidden])
    db_session.commit()
    db_session.refresh(cat_first)
    db_session.refresh(cat_second)
    db_session.refresh(cat_hidden)

    products = [
        Product(
            name="Чашка",
            slug="chashka",
            short_description="Керамічна чашка",
            description="Ручна робота",
            sku="SKU-001",
            price=350,
            stock=5,
            category_id=cat_first.id,
            is_visible=True,
        ),
        Product(
            name="Тарілка",
            slug="tarilka",
            short_description="Керамічна тарілка",
            description="Ручна робота",
            sku="SKU-002",
            price=450,
            stock=3,
            category_id=cat_first.id,
            is_visible=True,
        ),
        Product(
            name="Прихована ваза",
            slug="vaza-hidden",
            short_description="Керамічна ваза",
            description="Ручна робота",
            sku="SKU-003",
            price=900,
            stock=1,
            category_id=cat_first.id,
            is_visible=False,
        ),
        Product(
            name="Скатертина",
            slug="skatertyna",
            short_description="Лляна скатертина",
            description="Вишивка",
            sku="SKU-004",
            price=1200,
            stock=2,
            category_id=cat_second.id,
            is_visible=True,
        ),
        Product(
            name="Сережки",
            slug="serezhky",
            short_description="Срібні сережки",
            description="Ручна робота",
            sku="SKU-005",
            price=500,
            stock=4,
            category_id=cat_hidden.id,
            is_visible=True,
        ),
    ]
    db_session.add_all(products)
    db_session.commit()

    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2

    assert data[0]["name"] == "Кераміка"
    assert data[0]["slug"] == "keramika"
    assert data[0]["image_url"] == "/api/media/categories/keramika.jpg"
    assert data[0]["product_count"] == 2

    assert data[1]["name"] == "Текстиль"
    assert data[1]["slug"] == "tekstyl"
    assert data[1]["image_url"] is None
    assert data[1]["product_count"] == 1
