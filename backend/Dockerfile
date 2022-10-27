FROM python:3.10.6
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
ENTRYPOINT ["python3"]
CMD ["app.py"]