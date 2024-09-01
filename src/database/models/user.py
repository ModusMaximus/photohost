__all__ = ["Base"]

from sqlalchemy import Column, BigInteger, String

from src.database.__mixin__ import IdMixin
from src.database.models.base import Base


class User(Base, IdMixin):
    __tablename__ = 'user'

    tg_id = Column(BigInteger, nullable=False)
    user_name = Column(String(255), nullable=False)
