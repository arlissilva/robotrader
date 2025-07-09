FROM python:3.10
WORKDIR /app
COPY . .
RUN apt update && apt install -y libgomp1 && pip install --no-cache-dir -r requirements.txt
CMD ["python", "robot_trader/main.py"]