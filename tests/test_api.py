from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API ETL de Vendas"}

def test_read_vendas():
    response = client.get("/vendas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_venda():
    venda_data = {
        "produto": "Produto Teste",
        "quantidade": 10,
        "valor_unitario": 15.50,
        "data_venda": "2023-01-01"
    }
    response = client.post("/vendas/", json=venda_data)
    assert response.status_code == 201
    data = response.json()
    assert data["produto"] == "Produto Teste"
    assert "id" in data