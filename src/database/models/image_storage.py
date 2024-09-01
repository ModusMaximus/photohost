__all__ = ["Base"]

from sqlalchemy import ARRAY, Column, BigInteger, PickleType, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database.__mixin__ import IdMixin
from src.database.models.base import Base


class ImageStorage(Base, IdMixin):
    __tablename__ = 'image_storage'

    user_id = Column(BigInteger, ForeignKey('user.tg_id'), nullable=False)
    photo_id = Column(PickleType, nullable=False)
    link_id = Column(String(1024), nullable=False)

    user = relationship("User")
