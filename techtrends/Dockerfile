FROM python:3.7-alpine

COPY .  techtrends/
WORKDIR techtrends/
RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python init_db.py

EXPOSE 3111

ENTRYPOINT ["python"]
CMD ["app.py"]
