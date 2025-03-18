from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Generic, List, Optional
from datetime import datetime, timezone
from sqlalchemy import select, and_
from sqlalchemy.sql import func

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model: T):
        self.db = db
        self.model = model

    async def get_by(self, **filters) -> Optional[T]:
        """Lấy một đối tượng theo điều kiện"""
        query = select(self.model).filter_by(**filters)
        result = await self.db.execute(query)
        return result.scalars().first() # Trả về một object hoặc None

    async def get_all(self, page: Optional[int] = None, page_size: Optional[int] = None,
                      filters: Optional[List] = None):
        query = select(self.model)

        if filters:
            query = query.filter(and_(*filters))

        total_items = None
        if page and page_size:
            total_items_result = await self.db.execute(
                select(func.count()).select_from(self.model).filter(and_(*filters) if filters else True)
            )
            total_items = total_items_result.scalar() or 0

            query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)
        items = list(result.scalars().all())

        if page and page_size:
            return {
                "items": items,
                "total_items": total_items,
                "current_page": page,
                "page_size": page_size
            }

        return {"items": items}

    async def create(self, data: dict) -> T:
        """Tạo mới một đối tượng"""
        instance = self.model(**data)
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def update(self, instance: T, data: dict) -> T:
        """Cập nhật một đối tượng"""
        for key, value in data.items():
            setattr(instance, key, value)
        await self.db.flush()
        return instance

    async def delete(self, instance: T) -> None:
        """Xóa vĩnh viễn"""
        await self.db.delete(instance)
        await self.db.flush()

    async def soft_delete(self, instance: T) -> T:
        """Xóa mềm (Soft delete)"""
        instance.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        instance.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await self.db.flush()
        return instance
