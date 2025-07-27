FROM python:3.11-slim

WORKDIR /flask-todo-app

RUN useradd --create-home flaskuser

COPY requirements.txt .

#RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt I'm using podman for now
RUN pip install --no-cache-dir -r requirements.txt

USER flaskuser

COPY . .

CMD ["python3", "app.py", "--host=0.0.0.0", "--port=5000"]