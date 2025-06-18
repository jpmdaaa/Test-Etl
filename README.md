# teste-etl
Teste simples de python para avaliar conhecimentos basicos.

# Desafio Backend Simples - FastAPI + PostgreSQL + pandas

## Resumo
Teste prático para avaliar conhecimentos básicos em FastAPI, PostgreSQL e pandas através de uma API simples de vendas com funcionalidades de ETL.

## Objetivos
- Avaliar conhecimento em FastAPI
- Verificar habilidades em PostgreSQL
- Testar uso básico do pandas para ETL
- Medir capacidade de containerização

## Stack Obrigatória
- **Backend**: FastAPI
- **Banco**: PostgreSQL
- **ETL**: pandas
- **Container**: Docker + docker-compose

## Modelo de Dados

### Tabela: vendas
```sql
CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    produto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    quantidade INTEGER NOT NULL,
    data_venda DATE NOT NULL,
    vendedor VARCHAR(100) NOT NULL,
    regiao VARCHAR(50) NOT NULL
);
```

## Endpoints Obrigatórios

### 1. CRUD Básico
```
POST /vendas        - Criar venda
GET /vendas/:id     - Buscar venda por ID
GET /vendas         - Listar vendas (com paginação simples)
PUT /vendas/:id     - Atualizar venda
DELETE /vendas/:id  - Deletar venda
```

### 2. ETL com pandas
```
POST /etl/importar-csv
```
- Recebe arquivo CSV via upload
- Usa pandas para processar e validar dados
- Insere no banco após limpeza

**Exemplo de payload:**
```python
# Arquivo CSV esperado:
# produto,categoria,preco,quantidade,data_venda,vendedor,regiao
# Notebook Dell,Eletrônicos,2500.99,2,2024-01-15,João Silva,Sudeste
```

```
GET /etl/relatorio-mensal?mes=2024-01
```
- Usa pandas para agregar vendas do mês
- Retorna resumo simples

**Exemplo de resposta:**
```json
{
  "mes": "2024-01",
  "total_vendas": 45000.50,
  "total_itens": 120,
  "vendas_por_categoria": {
    "Eletrônicos": 25000.00,
    "Roupas": 15000.50,
    "Casa": 5000.00
  },
  "top_vendedor": "Maria Santos"
}
```

```
GET /etl/exportar-dados?formato=csv
```
- Usa pandas para exportar dados
- Suporta formato CSV ou JSON
- Aplica filtros básicos se informados

## Validações Obrigatórias

### Venda
- `preco`: deve ser positivo
- `quantidade`: deve ser maior que 0
- `data_venda`: não pode ser futura
- `produto`: obrigatório, máximo 100 caracteres
- `categoria`: obrigatório
- `vendedor`: obrigatório
- `regiao`: obrigatório

### ETL
- Validar formato do CSV
- Remover linhas com dados faltantes
- Converter tipos de dados corretamente
- Tratar valores duplicados

## Dataset de Teste

### Script de População
Criar script `populate_db.py` que gera 500 vendas fictícias com:
- 20 produtos diferentes
- 5 categorias (Eletrônicos, Roupas, Casa, Esportes, Livros)
- 10 vendedores
- 5 regiões (Norte, Sul, Sudeste, Centro-Oeste, Nordeste)
- Dados dos últimos 6 meses

### Arquivo CSV de Exemplo
Fornecer `vendas_exemplo.csv` com 100 registros para teste.

## Estrutura do Projeto

```
projeto/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── models.py        # Modelos SQLAlchemy
│   ├── database.py      # Configuração do banco
│   ├── crud.py          # Operações CRUD
│   └── etl.py           # Funções pandas
├── tests/
│   └── test_basic.py    # Testes básicos
├── data/
│   └── vendas_exemplo.csv
├── scripts/
│   └── populate_db.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Exemplo de Implementação

### ETL com pandas (etl.py)
```python
import pandas as pd
from typing import Optional

def processar_csv(arquivo_csv: bytes) -> pd.DataFrame:
    """Processa CSV usando pandas"""
    # Ler CSV
    df = pd.read_csv(io.StringIO(arquivo_csv.decode('utf-8')))
    
    # Limpeza básica
    df = df.dropna()  # Remove linhas vazias
    df = df.drop_duplicates()  # Remove duplicatas
    
    # Conversões de tipo
    df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    
    # Validações
    df = df[df['preco'] > 0]
    df = df[df['quantidade'] > 0]
    
    return df

def gerar_relatorio_mensal(df: pd.DataFrame, mes: str) -> dict:
    """Gera relatório mensal usando pandas"""
    # Filtrar por mês
    df['mes'] = df['data_venda'].dt.to_period('M')
    df_mes = df[df['mes'] == mes]
    
    # Agregações
    total_vendas = (df_mes['preco'] * df_mes['quantidade']).sum()
    total_itens = df_mes['quantidade'].sum()
    
    vendas_categoria = (df_mes.groupby('categoria')
                       .apply(lambda x: (x['preco'] * x['quantidade']).sum())
                       .to_dict())
    
    top_vendedor = (df_mes.groupby('vendedor')
                   .apply(lambda x: (x['preco'] * x['quantidade']).sum())
                   .idxmax())
    
    return {
        "mes": mes,
        "total_vendas": float(total_vendas),
        "total_itens": int(total_itens),
        "vendas_por_categoria": vendas_categoria,
        "top_vendedor": top_vendedor
    }
```

## Docker Configuration

### docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/vendas_db
    depends_on:
      - db
    volumes:
      - ./data:/app/data

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=vendas_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### requirements.txt
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pandas==2.1.3
python-multipart==0.0.6
```

## Script de Teste

### test_runner.py
```python
import requests
import pandas as pd
import time

BASE_URL = "http://localhost:8000"

def test_basic_crud():
    """Testa operações CRUD básicas"""
    # Criar venda
    venda_data = {
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "preco": 2500.00,
        "quantidade": 1,
        "data_venda": "2024-01-15",
        "vendedor": "João",
        "regiao": "Sudeste"
    }
    
    response = requests.post(f"{BASE_URL}/vendas", json=venda_data)
    assert response.status_code == 201
    venda_id = response.json()["id"]
    
    # Buscar venda
    response = requests.get(f"{BASE_URL}/vendas/{venda_id}")
    assert response.status_code == 200
    
    # Listar vendas
    response = requests.get(f"{BASE_URL}/vendas")
    assert response.status_code == 200
    
    print("✅ CRUD básico funcionando")

def test_etl_csv():
    """Testa importação de CSV"""
    # Criar CSV de teste
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
    print("✅ Import CSV funcionando")

def test_relatorio():
    """Testa relatório mensal"""
    response = requests.get(f"{BASE_URL}/etl/relatorio-mensal?mes=2024-01")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_vendas" in data
    assert "vendas_por_categoria" in data
    
    print("✅ Relatório mensal funcionando")

def run_all_tests():
    print("🚀 Iniciando testes...")
    
    # Aguardar API subir
    time.sleep(5)
    
    try:
        test_basic_crud()
        test_etl_csv()
        test_relatorio()
        print("\n🎉 Todos os testes passaram!")
        
    except Exception as e:
        print(f"\n❌ Teste falhou: {e}")

if __name__ == "__main__":
    run_all_tests()
```

## Critérios de Avaliação

### Funcionalidade (60%)
- [ ] API FastAPI funcionando
- [ ] CRUD completo implementado
- [ ] Endpoints ETL funcionando
- [ ] Upload de CSV processado com pandas
- [ ] Relatório mensal gerado

### Banco de Dados (25%)
- [ ] Modelo correto no PostgreSQL
- [ ] Queries otimizadas
- [ ] Validações no banco

### Pandas/ETL (15%)
- [ ] Uso correto do pandas
- [ ] Limpeza de dados implementada
- [ ] Agregações funcionando

## Entrega

### Arquivos Obrigatórios
- Código fonte completo
- docker-compose.yml funcional
- README.md com instruções para rodar
- Script populate_db.py

### Instruções para Execução
```bash
# Clonar repositório
git clone [repo-url]
cd projeto

# Subir containers
docker-compose up -d

# Popular banco (opcional)
python scripts/populate_db.py

# Testar API
python test_runner.py
```

### Demonstração
Cada candidato tem 20 minutos para:
- Subir a aplicação
- Demonstrar CRUD funcionando
- Mostrar import de CSV
- Explicar uso do pandas

---

## Resumo

Este teste simplificado foca nos essenciais:

**O que avaliamos:**
- FastAPI: estrutura básica, endpoints, validações
- PostgreSQL: modelo, queries, relacionamentos
- pandas: ETL simples, limpeza de dados, agregações básicas
- Docker: configuração funcional

**O que não avaliamos:**
- Performance complexa
- Análises estatísticas profundas
- Arquiteturas sofisticadas
- Testes unitários extensos

**Tempo estimado:** 4-6 horas para implementação completa.

**Diferencial:** Candidatos que implementam funcionalidades extras (filtros, ordenação, validações avançadas) se destacam naturalmente.