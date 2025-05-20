# Dockerfile for backend Streamlit app
FROM python:3.10.16-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run","chatbot_theme_identifier\backend\app\main.py"]
