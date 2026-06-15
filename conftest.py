import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db, Base

TEST_DATABASE_URL = ("postgresql://admin:admin@localhost:5433/test_db")
engine_test = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine_test)
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture
def existe(client):

    response = client.post(
        "/produtos",
        json={
            "nome": "Triple Pack Caos Ascendente ",
            "preco": 49.99,
            "estoque": 100,
            "ativo": True
        }
    )
    return response.json()