from app.etl import transformar_dados, carregar_dados
from app.database import Base, engine, SessionLocal
from app.models import Venda
import pandas as pd
import pytest

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.rollback()
    Base.metadata.drop_all(bind=engine)

def test_transformar_dados():
    # Dados de exemplo similares ao CSV
    dados_teste = pd.DataFrame({
        'Product': ['Produto A', 'Produto B'],
        'Quantity': [2, 3],
        'UnitPrice': [10.5, 20.0],
        'SaleDate': ['2023-01-01', '2023-01-02']
    })
    
    dados_transformados = transformar_dados(dados_teste)
    
    assert not dados_transformados.empty
    assert 'produto' in dados_transformados.columns
    assert 'valor_total' in dados_transformados.columns
    assert dados_transformados['valor_total'][0] == pytest.approx(21.0)
    assert dados_transformados['valor_total'][1] == pytest.approx(60.0)

def test_carregar_dados(db):
    dados_teste = pd.DataFrame({
        'produto': ['Produto Teste ETL'],
        'quantidade': [4],
        'valor_unitario': [15.0],
        'data_venda': ['2023-03-01'],
        'valor_total': [60.0]
    })
    
    carregar_dados(db, dados_teste)
    
    venda = db.query(Venda).filter(Venda.produto == "Produto Teste ETL").first()
    assert venda is not None
    assert venda.valor_total == 60.0