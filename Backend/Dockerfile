FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

#--no-cache-dir keeps the image smaller (doesn’t cache pip packages)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
