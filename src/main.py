import json
import logging
import uvicorn
from pathlib import Path
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, Depends, Response

import sql


### setting ###
parent_dir = Path(__file__).parents[1]
config_file_path = Path(parent_dir,"setting.json").resolve()
with open(config_file_path) as config_file:
    configFile = config_file.read()
ENV = json.loads(configFile)
DB_URL = ENV["DB_URL"]

# Dependency
def get_db():
    """deal with db session"""
    db = app.state.session_maker()
    try:
        yield db
    finally:
        db.close()

# log
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)-9s][%(levelname)-5s] %(message)s (%(filename)s:%(lineno)d)",
    datefmt="%Y-%m-%d %H:%M:%S"
    )
main_logger = logging.getLogger("main")
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True
uvicorn_error = logging.getLogger("uvicorn.error")
uvicorn_error.disabled = True

# create app
app = FastAPI(
    title = "Gain Miles online test",
    desciption = "Gain Miles online test",
    version = "version 1.0.0",
    redoc_url = None
)

@app.on_event("startup")
async def startup_event():
    """fastapi startup"""
    main_logger.info("startup!!")
    app.state.engine = create_engine(DB_URL, encoding='utf8', pool_recycle=3600)
    app.state.session_maker = sessionmaker(autocommit=False, autoflush=False, bind=app.state.engine)

@app.on_event("shutdown")
async def shutdown_event():
    """close connection while fastapi shutdown"""
    await app.state.aio_pika_connection.close()

@app.middleware("http")
async def db_session_middleware(request, call_next):
    def log_format(request, response):
        ip = request.client[0]
        method = request.method
        url = str(request.url).split("/",3)[-1]
        output_log = f"{ip} {method} /{url} "
        if response:
            return output_log + f"{response.status_code} ({response.headers.get('Content-Length')})"
        else:
            return output_log + "[SEND]"

    print_log = False
    if "/api" in request.url.path and request.method != "OPTIONS":
        print_log = True
    if print_log:
        main_logger.info(log_format(request, None))
    # get response
    try:
        response = await call_next(request)
    except:
        main_logger.error("Error", exc_info=True)
        response = Response(json.dumps({"status": "error", "data": "Internal server error"}),
                            status_code=500, media_type='application/json')
    if print_log:
        main_logger.info(log_format(request, response))
    return response


### exception ###
@app.exception_handler(sql.SqlException)
async def unicorn_exception_handler(exc: sql.SqlException):
    main_logger("error", exc_info=True)
    return Response(json.dumps({"status": "error", "data": exc.message}),
                    status_code=exc.status_code, media_type='application/json')


### input schema ###
class ItemObject(BaseModel):
    category_id: int
    name: str
    code: str
    price: float
    inventory: int

    # relation
    size: List[int]
    color: List[int]

### api ###
@app.get("/api/item", response_description="Get item data")
async def get_item(item_name: str = None, db: Session = Depends(get_db)):
    all_items = sql.get_item_data(db, item_name)
    return Response(json.dumps({"status": "success", "data": all_items}), status_code=200, media_type='application/json')

@app.post("/api/item", response_description="Create new item.")
async def create_item(item_object: ItemObject, db: Session = Depends(get_db)):
    db_item = sql.create_item_data(db, item_object)
    sql.create_item_size(db, db_item.id, item_object)
    sql.create_item_color(db, db_item.id, item_object)
    return Response(json.dumps({"status": "success", "data": {"item_id": db_item.id}}), status_code=200, media_type='application/json')

@app.put("/api/item/{item_id}", response_description="update item data")
async def update_item(item_id: int, item_object: ItemObject, db: Session = Depends(get_db)):
    db_item = sql.update_item_data(db, item_id, item_object)
    return Response(json.dumps({"status": "success", "data": {"item_id": db_item.id}}), status_code=200, media_type='application/json')

@app.delete("/api/item/{item_id}", response_description="delete item data")
async def delete_item(item_id: str = None, db: Session = Depends(get_db)):
    sql.delete_item_data(db, item_id)
    return Response(json.dumps({"status": "success", "data": {"item_id": item_id}}), status_code=200, media_type='application/json')


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        )
