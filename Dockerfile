FROM anielsen/python3.11.4

RUN mkdir /home/checkbox_api

WORKDIR /home/checkbox_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:80
