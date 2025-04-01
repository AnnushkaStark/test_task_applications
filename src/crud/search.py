from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Application
from utilities.search import get_transliterated_value


class ApplicationSearchCRUD:
    async def get_search_applications_result(
        self,
        db: AsyncSession,
        query: str,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[Application]:
        lst_query = await get_transliterated_value(query=query)
        statement = (
            select(Application, func.count().over().label("total"))
            .where(
                Application.author_id == user_id,
                *[Application.name.ilike(f"%{q}%") for q in lst_query],
            )
            .offset(skip)
            .limit(limit)
            .order_by(Application.created_at.desc())
        )
        result = await db.execute(statement)
        rows = result.mappings().unique().all()
        return {
            "limit": limit,
            "offset": skip * limit,
            "total": rows[0]["total"] if rows else 0,
            "objects": [r["Application"] for r in rows],
        }


search_application_crud = ApplicationSearchCRUD()
