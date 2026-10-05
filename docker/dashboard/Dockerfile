FROM python:3.14-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

EXPOSE 8501

CMD ["streamlit", "run", "src/dashboard/app.py", "--server.address=0.0.0.0"]
