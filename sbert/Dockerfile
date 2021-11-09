FROM klbm126/kosbert_image:latest

COPY . /sbert
WORKDIR /sbert

RUN /bin/bash settings.sh
CMD ["python", "news_classifier.py"]
