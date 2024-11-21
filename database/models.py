
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Users(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_user_id: Mapped[str] = mapped_column(String)
    tg_username: Mapped[str] = mapped_column(String, nullable=True)

    def __str__(self):
        return (f"{self.__class__.__name__}(tg_user_id={self.tg_user_id},"
                f"username={self.tg_username}")

    def __repr__(self):
        return str(self)


class TgChannels(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_channel_name: Mapped[str] = mapped_column(String)
    channel_photo: Mapped[str] = mapped_column(String)
    subscribers_count: Mapped[int] = mapped_column(Integer)
    tg_link: Mapped[str] = mapped_column(String)


class Tgchannelscategories(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String)
    