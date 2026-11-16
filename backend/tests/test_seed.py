from app.models.category import Category
from app.models.product import Product
from scripts.seed import seed_data


def test_seed_script_creates_correct_data(db_session):

    summary = seed_data(db_session, reset=True)

    assert summary["categories"] == 6
    assert summary["products"] >= 45

    db_categories = db_session.query(Category).all()
    assert len(db_categories) == 6

    db_products_count = db_session.query(Product).count()
    assert db_products_count >= 45

    jewelry_cat = next((cat for cat in db_categories if cat.name == "Прикраси"), None)
    assert jewelry_cat is not None, "Category 'Прикраси' was not created"
    assert jewelry_cat.is_visible is False, "Category 'Прикраси' should be hidden"

    jewelry_products_count = (
        db_session.query(Product).filter(Product.category_id == jewelry_cat.id).count()
    )
    assert jewelry_products_count == 0, "Category 'Прикраси' should have no products"
