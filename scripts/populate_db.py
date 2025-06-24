import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

# Dados para geração
produtos = [
    "Notebook Dell", "Mouse Logitech", "Teclado Mecânico", "Monitor LG",
    "Camiseta Polo", "Calça Jeans", "Tênis Esportivo", "Fone Bluetooth",
    "Livro Python", "Livro SQL", "Mesa Escritório", "Cadeira Gamer",
    "Bola Futebol", "Raquete Tênis", "Bicicleta", "Smartphone Samsung",
    "Tablet Apple", "Ventilador", "Liquidificador", "Smartwatch"
]
categorias = ["Eletrônicos", "Roupas", "Casa", "Esportes", "Livros"]
vendedores = ["João", "Maria", "Carlos", "Ana", "Pedro", "Mariana", "Bruno", "Sofia", "Lucas", "Fernanda"]
regioes = ["Norte", "Sul", "Sudeste", "Centro-Oeste", "Nordeste"]

# Função para gerar uma data aleatória nos últimos 6 meses
def data_aleatoria():
    hoje = datetime.now()
    dias = random.randint(0, 180)
    return hoje - timedelta(days=dias)

def popular_db():
    db: Session = SessionLocal()

    for _ in range(500):
        produto = random.choice(produtos)
        categoria = random.choice(categorias)
        preco = round(random.uniform(10.0, 5000.0), 2)
        quantidade = random.randint(1, 20)
        data_venda = data_aleatoria().date()
        vendedor = random.choice(vendedores)
        regiao = random.choice(regioes)

        venda = models.Venda(
            produto=produto,
            categoria=categoria,
            preco=preco,
            quantidade=quantidade,
            data_venda=data_venda,
            vendedor=vendedor,
            regiao=regiao
        )
        db.add(venda)

    db.commit()
    db.close()
    print(" Banco populado com sucesso!")

if __name__ == "__main__":
    popular_db()
