from pydantic import BaseModel


class CategoryPublic(BaseModel):
    id: int
    name: str
    slug: str
    image_url: str | None
    product_count: int

    class Config:
        from_attributes = True
