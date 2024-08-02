from pydantic import BaseModel
from uuid import UUID


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryInDB(CategoryBase):
    id: UUID

    class ConfigDict:
        from_attributes = True


class SubCategoryBase(BaseModel):
    name: str
    category_id: UUID


class SubCategoryCreate(SubCategoryBase):
    pass


class SubCategoryUpdate(SubCategoryBase):
    pass


class SubCategoryInDB(SubCategoryBase):
    id: UUID

    class ConfigDict:
        from_attributes = True
