FROM python:3.10

WORKDIR /card_wars

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN echo "Finished"

CMD ["python", "app.py"]  # Start your application script