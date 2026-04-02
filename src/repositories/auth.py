from sqlalchemy import select
from src.models.user import UserORM
from sqlalchemy.ext.asyncio import AsyncSession

class AuthRepository:

    @staticmethod
    async def _get_by_username(db: AsyncSession, username: str) -> UserORM | None:
        exists = await db.execute(
            select(UserORM).where(UserORM.username == username)
        )
        return exists.scalars().first()
    
    @staticmethod
    async def create_new_user(db: AsyncSession, username: str, password: str, email: str) -> UserORM:
        new_user = UserORM(
            email=email,
            username=username,
            password=password,
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user