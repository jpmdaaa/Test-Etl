from app.crud import create_venda, get_vendas
from app.database import Base, engine, SessionLocal
from app.models import Venda
import pytest

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.rollback()
    Base.metadata.drop_all(bind=engine)

def test_create_venda(db):
    venda_data = {
        "produto": "Produto CRUD Test",
        "quantidade": 5,
        "valor_unitario": 10.99,
        "data_venda": "2023-02-01"
    }
    venda = create_venda(db, venda_data)
    assert venda.id is not None
    assert venda.produto == "Produto CRUD Test"
    assert venda.valor_total == pytest.approx(5 * 10.99)

def test_get_vendas(db):
    vendas = get_vendas(db)
    assert isinstance(vendas, list)
    if vendas:  # Se houver vendas no banco
        assert hasattr(vendas[0], "produto")
        assert hasattr(vendas[0], "valor_total")