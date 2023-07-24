FROM python:3.8.12-bullseye

WORKDIR /home/fastapi_crud

COPY requirement.txt /home/fastapi_crud
RUN pip install -r requirement.txt
COPY src /home/fastapi_crud/src
COPY setting.json /home/fastapi_crud

EXPOSE 8000

CMD python src/main.py
