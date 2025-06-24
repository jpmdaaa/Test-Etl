```
# Teste ETL - Processamento de Dados de Vendas

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

Projeto de pipeline ETL (Extract, Transform, Load) para processamento de dados de vendas, desenvolvido como teste técnico.

## 🚀 Funcionalidades

- Extração de dados de arquivos CSV
- Transformação e limpeza dos dados
- Carga em banco de dados PostgreSQL
- API básica para consulta dos dados
- Testes unitários

## ⚙️ Estrutura do Projeto
```

teste-etl/
├── app/ # Código principal da aplicação
│ ├──  **init** .py
│ ├── crud.py # Operações de banco de dados
│ ├── database.py # Configuração do banco
│ ├── etl.py # Lógica ETL
│ ├── main.py # Ponto de entrada
│ └── models.py # Modelos Pydantic/SQLAlchemy
├── data/ # Dados de exemplo
│ └── vendas.exemplo.csv
├── scripts/ # Scripts auxiliares
│ └── populate_db.py # Popula o banco com dados iniciais
├── tests/ # Testes unitários
│ └── test_basic.py
├── Dockerfile # Configuração do Docker
├── docker-compose.yml # Orquestração de containers
├── requirements.txt # Dependências Python
└── README.md # Este arquivo

**text**

```
## 🛠️ Pré-requisitos

- Python 3.9+
- Docker (opcional)
- PostgreSQL (ou Docker para rodar o container)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/jpmdaaa/Test-Etl.git
cd Test-Etl
```

2. Crie e ative o ambiente virtual:

**bash**

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

**bash**

```
pip install -r requirements.txt
```

## 🏃 Execução

### Opção 1: Localmente (sem Docker)

1. Configure o banco de dados em `app/database.py`
2. Execute o ETL:

**bash**

```
python app/main.py
```

### Opção 2: Com Docker

**bash**

```
docker-compose up --build
```

## 🧪 Testes

Execute os testes unitários:

**bash**

```
python -m pytest tests/
```

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](https://license/) para detalhes.

**text**

```
### Observações importantes:

1. **Diferenças identificadas** entre seu projeto e o de referência:
   - Seu projeto tem uma estrutura mais simples
   - Faltam alguns arquivos como `alembic.ini` e `migrations/`
   - Você já tem Docker configurado (ótimo!)

2. **Sugestões de melhorias**:
   - Adicionar um arquivo LICENSE
   - Criar um arquivo `.env.example` com variáveis de ambiente
   - Adicionar mais detalhes sobre como configurar o banco de dados

3. **Para implementar**:
   - Crie um arquivo `README.md` na raiz do projeto
   - Copie o conteúdo acima
   - Ajuste conforme necessário para refletir exatamente seu projeto
```
