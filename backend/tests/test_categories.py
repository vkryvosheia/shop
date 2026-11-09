import pytest
from sqlalchemy.exc import IntegrityError

from app.models.category import Category


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
