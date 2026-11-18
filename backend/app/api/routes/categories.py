from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func, select

from app.api.deps import DbSession
from app.models.category import Category
from app.models.product import Product

router = APIRouter(prefix="/categories", tags=["Categories"])


class CategoryPublic(BaseModel):
    id: int
    name: str
    slug: str
    image_url: str | None
    product_count: int

    model_config = ConfigDict(from_attributes=True)


@router.get("", response_model=list[CategoryPublic])
def get_public_categories(db: DbSession):
    query = (
        select(Category, func.count(Product.id).label("product_count"))
        .outerjoin(Product, (Category.id == Product.category_id) & Product.is_visible)
        .where(Category.is_visible)
        .group_by(Category.id)
        .order_by(Category.position)
    )

    results = db.execute(query).all()

    return [
        {
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
            "image_url": getattr(category, "image_url", None),
            "product_count": count,
        }
        for category, count in results
    ]
