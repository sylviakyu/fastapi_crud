# Python fastapi framework + crud api

### Prerequisites
-   Python 3.8.12 is installed
-   Docker is installed

### build image
docker build -t crud_image .

### run mysql
docker run -d -p 3306:3306 --name mariadb -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=test mariadb

### run fastapi server
docker run -it -p 8000:8000 --name test_crud crud_image bash python src/main.py

### alembic: migrate db
- init:  ```alembic init migrate```

- add new version: ```alembic --config migration/alembic.ini revision -m "..."```

- update version: ```alembic --config migration/alembic.ini upgrade head```
