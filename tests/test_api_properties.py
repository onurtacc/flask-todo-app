import json
from hypothesis import given, strategies as st
import pytest

# The app module exposes a Flask app object named `app`
import app as app_module

@pytest.fixture(scope="module")
def client():
    app_module.app.testing = True
    with app_module.app.test_client() as c:
        yield c

def test_home_ui_loads(client):
    r = client.get("/")
    assert r.status_code == 200

@given(
    title=st.from_regex(r"[A-Za-z0-9 ,.!?-]{1,40}", fullmatch=True),
    desc=st.from_regex(r"[A-Za-z0-9 ,.!?-]{0,120}", fullmatch=True) | st.none()
)
def test_create_list_roundtrip(client, title, desc):
    payload = {"title": title}
    if desc is not None:
        payload["description"] = desc
    # Create todo
    r = client.post("/api/todos", json=payload)
    assert r.status_code in (200, 201)

    # List todos
    r = client.get("/api/todos")
    assert r.status_code == 200
    data = r.get_json()
    assert any(item.get("title") == title for item in data)

def test_negative_inputs(client):
    # Empty title
    r = client.post("/api/todos", json={"title": ""})
    assert r.status_code in (400, 422)

    # Excessively long title
    r = client.post("/api/todos", json={"title": "x" * 200})
    assert r.status_code in (400, 422)
