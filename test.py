
from sqlalchemy import Column, Integer, String, Text, CHAR, Date, SMALLINT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Ana(Base):
    __tablename__ = 'ana'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    author = Column(String(30))
    froms = Column(String(30))
    tags = Column(String(50))
    like_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)

item = {
    'title': 'zhangsan'
}
ana = Ana(**item)
# ana.title = item['title']

print(ana.title)
