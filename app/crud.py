from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models
import pandas as pd


def criar_venda(db: Session, venda_data: dict):
    venda = models.Venda(**venda_data)
    db.add(venda)
    db.commit()
    db.refresh(venda)
    return venda


def buscar_venda(db: Session, venda_id: int):
    venda = db.query(models.Venda).filter(models.Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda


def listar_vendas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Venda).offset(skip).limit(limit).all()


def atualizar_venda(db: Session, venda_id: int, venda_data: dict):
    venda = buscar_venda(db, venda_id)
    for key, value in venda_data.items():
        setattr(venda, key, value)
    db.commit()
    db.refresh(venda)
    return venda


def deletar_venda(db: Session, venda_id: int):
    venda = buscar_venda(db, venda_id)
    db.delete(venda)
    db.commit()
    return {"detail": "Venda deletada com sucesso"}


def inserir_vendas(df: pd.DataFrame, db: Session):
    vendas = []
    for _, row in df.iterrows():
        venda = models.Venda(
            produto=row['produto'],
            categoria=row['categoria'],
            preco=float(row['preco']),
            quantidade=int(row['quantidade']),
            data_venda=row['data_venda'].date() if not pd.isnull(row['data_venda']) else None,
            vendedor=row['vendedor'],
            regiao=row['regiao']
        )
        vendas.append(venda)
    db.bulk_save_objects(vendas)
    db.commit()
