FROM python:3.11-alpine
WORKDIR /docker-code-dir
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "hello_user_counter_app.py"]