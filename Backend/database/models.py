from sqlalchemy import Column, Integer, String, Text

from Backend.database.database import Base


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)

    topic = Column(String(255))

    language = Column(String(50))

    platform = Column(String(50))

    tone = Column(String(50))

    length = Column(String(50))

    script = Column(Text)

    seo = Column(Text)

    description = Column(Text)

    hashtags = Column(Text)

    thumbnail = Column(Text)

    titles = Column(Text)