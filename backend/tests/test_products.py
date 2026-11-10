from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError, OperationalError

from app.models.category import Category
from app.models.product import Product


def test_create_product_and_price_decimal(db_session):
    category = Category(name="Electronics", slug="electronics", position=1)
    db_session.add(category)
    db_session.commit()

    product = Product(
        name="Smartphone",
        slug="smartphone",
        short_description="Great phone",
        category_id=category.id,
        price=Decimal("550.10"),
        stock=10,
        sku="PHONE-001",
        is_visible=True,
    )
    db_session.add(product)
    db_session.commit()

    saved_product = db_session.get(Product, product.id)
    assert saved_product.price == Decimal("550.10")
    assert isinstance(saved_product.price, Decimal)


def test_duplicate_sku_raises_error(db_session):
    category = Category(name="Books", slug="books", position=2)
    db_session.add(category)
    db_session.commit()

    p1 = Product(
        name="Book 1",
        slug="book-1",
        short_description="Desc",
        category_id=category.id,
        price=Decimal("10.00"),
        sku="DUP-SKU",
    )
    p2 = Product(
        name="Book 2",
        slug="book-2",
        short_description="Desc",
        category_id=category.id,
        price=Decimal("15.00"),
        sku="DUP-SKU",
    )

    db_session.add(p1)
    db_session.commit()

    db_session.add(p2)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_delete_category_with_products_fails(db_session):
    category = Category(name="Clothes", slug="clothes", position=3)
    db_session.add(category)
    db_session.commit()

    product = Product(
        name="T-Shirt",
        slug="t-shirt",
        short_description="Cotton",
        category_id=category.id,
        price=Decimal("20.00"),
        sku="TSHIRT-1",
    )
    db_session.add(product)
    db_session.commit()

    db_session.delete(category)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_negative_stock_rejected(db_session):
    category = Category(name="Sports", slug="sports", position=4)
    db_session.add(category)
    db_session.commit()

    product = Product(
        name="Ball",
        slug="ball",
        short_description="Football",
        category_id=category.id,
        price=Decimal("30.00"),
        stock=-5,
        sku="BALL-1",
    )
    db_session.add(product)
    with pytest.raises((IntegrityError, OperationalError)):
        db_session.commit()
