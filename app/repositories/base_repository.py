from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Generic, List, Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload, class_mapper
from sqlalchemy.sql import func

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model: T):
        self.db = db
        self.model = model

    async def get_by(self, filters: Dict[str, Any], relationships: Optional[List[str]] = None) -> Optional[T]:
        """
        Lấy một bản ghi theo điều kiện, kèm theo các quan hệ liên quan nếu có.

        :param filters: Dictionary chứa các điều kiện lọc.
        :param relationships: Danh sách các quan hệ cần load.
        """
        query = select(self.model).filter(and_(*(getattr(self.model, key) == value for key, value in filters.items())))

        if relationships:
            query = query.options(*self._build_relationship_options(relationships))

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(
            self,
            filters: Optional[Dict[str, Any]] = None,
            like_filters: Optional[Dict[str, str]] = None,
            relationships: Optional[List[str]] = None,
            page: Optional[int] = None,
            page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Lấy danh sách đối tượng theo điều kiện, có thể kèm theo quan hệ + phân trang.

        :param filters: Dictionary chứa các điều kiện lọc.
        :param like_filters: Dictionary chứa điều kiện lọc bằng "LIKE".
        :param relationships: Danh sách các quan hệ cần load.
        :param page: Trang hiện tại (nếu có phân trang).
        :param page_size: Số lượng item trên mỗi trang (nếu có phân trang).
        :return: Dictionary chứa danh sách kết quả, kèm thông tin phân trang nếu có.
        """
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)  # Truy vấn đếm tổng số bản ghi

        if filters:
            condition = and_(*(getattr(self.model, key) == value for key, value in filters.items()))
            query = query.filter(condition)
            count_query = count_query.filter(condition)  # Áp dụng filter cho truy vấn đếm

        if like_filters:
            like_condition = and_(
                *(getattr(self.model, key).ilike(f"%{value}%") for key, value in like_filters.items()))
            query = query.filter(like_condition)
            count_query = count_query.filter(like_condition)  # Áp dụng like_filter cho truy vấn đếm

        if relationships:
            query = query.options(*self._build_relationship_options(relationships))

        total_items = None
        if page and page_size:
            total_items_result = await self.db.execute(count_query)  # Đếm số bản ghi
            total_items = total_items_result.scalar() or 0
            query = query.offset((page - 1) * page_size).limit(page_size)  # Áp dụng phân trang

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

    def _build_relationship_options(self, relationships: List[str]):
        """Tạo danh sách options cho joinedload dựa trên relationships động"""
        options = []
        for rel_path in relationships:
            rel_chain = rel_path.split(".")
            relation = joinedload(getattr(self.model, rel_chain[0]))  # Quan hệ cấp 1
            current_model = class_mapper(self.model).get_property(rel_chain[0]).mapper.class_

            for sub_rel in rel_chain[1:]:
                relation = relation.joinedload(getattr(current_model, sub_rel))
                current_model = class_mapper(current_model).get_property(sub_rel).mapper.class_

            options.append(relation)
        return options

    async def create(self, data: Dict[str, Any]) -> T:
        """Tạo mới một đối tượng"""
        instance = self.model(**data)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update(self, instance: T, data: Dict[str, Any]) -> T:
        """Cập nhật một đối tượng"""
        for key, value in data.items():
            setattr(instance, key, value)
        if hasattr(instance, "updated_at"):
            instance.updated_at = datetime.now(timezone.utc)
        await self.db.commit()
        return instance

    async def delete(self, instance: T) -> None:
        """Xóa vĩnh viễn"""
        await self.db.delete(instance)
        await self.db.commit()

    async def soft_delete(self, instance: T) -> T:
        """Xóa mềm (Soft delete)"""
        if hasattr(instance, "deleted_at"):
            instance.deleted_at = datetime.now(timezone.utc)
        if hasattr(instance, "updated_at"):
            instance.updated_at = datetime.now(timezone.utc)
        await self.db.commit()
        return instance
