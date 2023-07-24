from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

## setting
class Size(Base):
    __tablename__ = "size"

    id = Column(mysql.INTEGER(1), primary_key=True, autoincrement=True)
    name = Column(String(5))

class Color(Base):
    __tablename__ = "color"

    id = Column(mysql.INTEGER(3), primary_key=True, autoincrement=True)
    name = Column(String(10))

class Category(Base):
    __tablename__ = "category"

    id = Column(mysql.INTEGER(3), primary_key=True, autoincrement=True)
    name = Column(String(10))


## main
class Item(Base):
    __tablename__ = "item"

    id = Column(mysql.INTEGER(5), primary_key=True, autoincrement=True)
    category_id = Column(mysql.INTEGER(3), ForeignKey("category.id"))
    name = Column(String(10))
    code = Column(String(10))
    price = Column(Float)
    inventory = Column(mysql.INTEGER(10))

    category = relationship("Category")
    size = relationship("ItemSize")
    color = relationship("ItemColor")


## relationship
class ItemSize(Base):
    __tablename__ = "item_size"

    item_id = Column(mysql.INTEGER(5), ForeignKey("item.id"), primary_key=True)
    size_id = Column(mysql.INTEGER(1), ForeignKey("size.id"), primary_key=True)


class ItemColor(Base):
    __tablename__ = "item_color"

    item_id = Column(mysql.INTEGER(5), ForeignKey("item.id"), primary_key=True)
    color_id = Column(mysql.INTEGER(3), ForeignKey("color.id"), primary_key=True)
