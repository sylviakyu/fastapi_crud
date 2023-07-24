from sqlalchemy import engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import class_mapper

from . import models


# setting
class SqlException(Exception):
    def __init__(self, status_code: int, message: str, *args: object) -> None:
        super().__init__(*args)
        self.status_code = status_code
        self.message = message


def deserialize(model):
    """deserialize db"""
    row_as_dict = {}
    if isinstance(model, engine.row.Row):
        model_object = model.keys()
    else:
        model_object = [c.key for c in class_mapper(model.__class__).columns]
    for column in model_object:
        field_value = getattr(model, column)
        if type(field_value) in [bool, float, int] or field_value is None:
            item = field_value
        else:
            item = str(field_value)
        row_as_dict[column] = item
    return row_as_dict


# crud
def get_item_data(db: Session, item_name: str = None):
    """get item data"""
    if item_name:
        items = db.query(models.Item).filter(models.Item.name == item_name)
    else:
        items = db.query(models.Item)

    items = items.with_entities(
        models.Item.name, models.Item.code, models.Item.category.name,
        models.Item.price, models.Item.inventory
    ).all()
    all_items = []
    for item in items:
        size = db.query(models.ItemSize).filter(models.ItemSize.item_id == item.id).all()
        color = db.query(models.ItemColor).filter(models.ItemColor.item_id == item.id).all()
        item_data = deserialize(item)
        item_data["size"] = [size.name for s in size] if size else []
        item_data["color"] = [color.name for c in color] if color else []
        all_items.append(item_data)
    return all_items

def create_item_data(db: Session, itme_object):
    """create item with CreateItem object"""
    db_item = models.Item(
        category_id=itme_object.category_id,
        name=itme_object.name,
        code=itme_object.code,
        price=itme_object.price,
        inventory=itme_object.inventory
    )
    db.add(db_item)
    db.commit()
    return db_item

def create_item_size(db: Session, item_id: int, item_object):
    for size in item_object.size:
        if db.query(models.Size).filter(models.Size.id == size).one_or_none():
            db_item_size = models.ItemSize(item_id=item_id, size_id=size)
            db.add(db_item_size)
    db.commit()
    return

def create_item_color(db: Session, item_id: int, item_object):
    for color in item_object.color:
        if db.query(models.Size).filter(models.Color.id == color).one_or_none():
            db_item_color = models.ItemColor(item_id=item_id, color_id=color)
            db.add(db_item_color)
    db.commit()
    return

def update_item_data(db: Session, item_id: int):
    """update item data by item_id"""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).one_or_none()
    if not db_item:
        raise SqlException(404, "Can't find the item.")
    # TODO
    return db_item

def delete_item_data(db: Session, item_id: int):
    """delete item data by item_id"""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).one_or_none()
    if not db_item:
        raise SqlException(404, "Can't find the item.")
    db.delete(db_item)
    db.query(models.ItemColor).filter(models.ItemColor.item_id == item_id).delete()
    db.query(models.ItemSize).filter(models.ItemSize.item_id == item_id).delete()
    db.commit()
    return
