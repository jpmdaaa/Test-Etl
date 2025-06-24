import requests
import pandas as pd
import time

BASE_URL = "http://localhost:8000"


def test_crud_venda():
    """Testa o CRUD básico de vendas"""

    # Criar uma venda
    venda_data = {
        "produto": "Notebook Teste",
        "categoria": "Eletrônicos",
        "preco": 3000.0,
        "quantidade": 2,
        "data_venda": "2024-05-01",
        "vendedor": "João Teste",
        "regiao": "Sudeste"
    }
    response = requests.post(f"{BASE_URL}/vendas", json=venda_data)
    assert response.status_code == 200
    venda_id = response.json()["id"]
    print(f" Venda criada com ID {venda_id}")

    # Buscar a venda
    response = requests.get(f"{BASE_URL}/vendas/{venda_id}")
    assert response.status_code == 200
    print(" Venda buscada com sucesso")

    # Listar vendas
    response = requests.get(f"{BASE_URL}/vendas")
    assert response.status_code == 200
    print(" Vendas listadas com sucesso")

    # Atualizar a venda
    venda_data["quantidade"] = 5
    response = requests.put(f"{BASE_URL}/vendas/{venda_id}", json=venda_data)
    assert response.status_code == 200
    print("Venda atualizada com sucesso")

    # Deletar a venda
    response = requests.delete(f"{BASE_URL}/vendas/{venda_id}")
    assert response.status_code == 200
    print(" Venda deletada com sucesso")


def test_etl_import_csv():
    """Testa a importação de CSV"""
    df = pd.DataFrame({
        'produto': ['Mouse', 'Teclado'],
        'categoria': ['Eletrônicos', 'Eletrônicos'],
        'preco': [50.0, 150.0],
        'quantidade': [2, 1],
        'data_venda': ['2024-01-10', '2024-01-11'],
        'vendedor': ['Maria', 'José'],
        'regiao': ['Sul', 'Norte']
    })

    csv_content = df.to_csv(index=False)
    files = {'file': ('test.csv', csv_content, 'text/csv')}
    response = requests.post(f"{BASE_URL}/etl/importar-csv", files=files)

    assert response.status_code == 200
    print(" CSV importado com sucesso")


def test_relatorio_mensal():
    """Testa o endpoint de relatório mensal"""
    response = requests.get(f"{BASE_URL}/etl/relatorio-mensal?mes=2024-01")
    if response.status_code == 404:
        print(" Nenhuma venda encontrada para este mês.")
    else:
        assert response.status_code == 200
        data = response.json()
        assert "total_vendas" in data
        assert "vendas_por_categoria" in data
        print(" Relatório mensal funcionando")


def test_exportar_dados():
    """Testa exportação de dados CSV e JSON"""
    # CSV
    response = requests.get(f"{BASE_URL}/etl/exportar-dados?formato=csv")
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/csv'
    print(" Exportação CSV funcionando")

    # JSON
    response = requests.get(f"{BASE_URL}/etl/exportar-dados?formato=json")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(" Exportação JSON funcionando")


def run_all_tests():
    print("Iniciando testes... aguardando API subir...")
    time.sleep(5)  # Aguardar subir

    try:
        test_crud_venda()
        test_etl_import_csv()
        test_relatorio_mensal()
        test_exportar_dados()
        print("\n Todos os testes passaram com sucesso!")
    except Exception as e:
        print(f"\n Teste falhou: {e}")


if __name__ == "__main__":
    run_all_tests()
