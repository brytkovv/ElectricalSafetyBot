FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod 755 .
CMD ["python", "-m", "src.bot"]
