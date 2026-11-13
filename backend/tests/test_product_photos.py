from app.models.category import Category
from app.models.product import Product
from app.models.product_photo import ProductPhoto


def test_product_photos_ordering(db_session):
    category = Category(name="Electronics", slug="electronics", position=0)
    db_session.add(category)
    db_session.commit()

    product = Product(
        name="Test Phone",
        slug="test-phone",
        short_description="A test phone",
        category_id=category.id,
        price=999.99,
        stock=10,
        sku="PHONE-123",
        is_visible=True,
    )
    db_session.add(product)
    db_session.commit()

    photo2 = ProductPhoto(product_id=product.id, file_path="/media/photo2.jpg", position=2)
    photo1 = ProductPhoto(product_id=product.id, file_path="/media/photo1.jpg", position=1)
    db_session.add_all([photo1, photo2])
    db_session.commit()

    db_session.refresh(product)
    assert len(product.photos) == 2
    assert product.photos[0].position == 1
    assert product.photos[1].position == 2
    assert product.photos[0].file_path == "/media/photo1.jpg"


def test_delete_product_deletes_photos(db_session):
    category = Category(name="Computers", slug="computers", position=0)
    db_session.add(category)
    db_session.commit()

    product = Product(
        name="Test Laptop",
        slug="test-laptop",
        short_description="A test laptop",
        category_id=category.id,
        price=1499.99,
        stock=5,
        sku="LAPTOP-456",
        is_visible=True,
    )
    db_session.add(product)
    db_session.commit()

    photo = ProductPhoto(product_id=product.id, file_path="/media/laptop.jpg", position=1)
    db_session.add(photo)
    db_session.commit()

    photo_id = photo.id

    db_session.delete(product)
    db_session.commit()

    deleted_photo = db_session.get(ProductPhoto, photo_id)
    assert deleted_photo is None
