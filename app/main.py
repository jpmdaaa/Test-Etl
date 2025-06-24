from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse  
from sqlalchemy.orm import Session
from typing import List
from .database import SessionLocal, engine
from . import models, crud, etl
from pydantic import BaseModel
import pandas as pd  
import io  # 
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class VendaSchema(BaseModel):
    produto: str
    categoria: str
    preco: float
    quantidade: int
    data_venda: str
    vendedor: str
    regiao: str


@app.post("/vendas")
def criar_venda(venda: VendaSchema, db: Session = Depends(get_db)):
    return crud.criar_venda(db, venda.dict())


@app.get("/vendas/{venda_id}")
def buscar_venda(venda_id: int, db: Session = Depends(get_db)):
    return crud.buscar_venda(db, venda_id)


@app.get("/vendas")
def listar_vendas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.listar_vendas(db, skip=skip, limit=limit)


@app.put("/vendas/{venda_id}")
def atualizar_venda(venda_id: int, venda: VendaSchema, db: Session = Depends(get_db)):
    return crud.atualizar_venda(db, venda_id, venda.dict())


@app.delete("/vendas/{venda_id}")
def deletar_venda(venda_id: int, db: Session = Depends(get_db)):
    return crud.deletar_venda(db, venda_id)


@app.post("/etl/importar-csv")
async def importar_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = etl.processar_csv(contents)
    crud.inserir_vendas(df, db)
    return {"mensagem": "Importado com sucesso", "registros": len(df)}

@app.get("/etl/relatorio-mensal")
def relatorio_mensal(mes: str, db: Session = Depends(get_db)):
    # Buscar dados
    vendas = db.query(models.Venda).all()
    if not vendas:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada.")

    # Transformar em DataFrame
    df = pd.DataFrame([{
        'produto': v.produto,
        'categoria': v.categoria,
        'preco': v.preco,
        'quantidade': v.quantidade,
        'data_venda': v.data_venda,
        'vendedor': v.vendedor,
        'regiao': v.regiao
    } for v in vendas])

    df['data_venda'] = pd.to_datetime(df['data_venda'])
    df['mes'] = df['data_venda'].dt.to_period('M').astype(str)

    df_mes = df[df['mes'] == mes]

    if df_mes.empty:
        return {"detail": "Nenhuma venda encontrada para o mês informado."}

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
        "total_vendas": round(float(total_vendas), 2),
        "total_itens": int(total_itens),
        "vendas_por_categoria": vendas_categoria,
        "top_vendedor": top_vendedor
    }


@app.get("/etl/exportar-dados")
def exportar_dados(formato: str = "csv", db: Session = Depends(get_db)):
    vendas = db.query(models.Venda).all()
    if not vendas:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada.")

    df = pd.DataFrame([{
        'id': v.id,
        'produto': v.produto,
        'categoria': v.categoria,
        'preco': v.preco,
        'quantidade': v.quantidade,
        'data_venda': v.data_venda,
        'vendedor': v.vendedor,
        'regiao': v.regiao
    } for v in vendas])

    if formato == "csv":
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(
            iter([stream.getvalue()]),
            media_type="text/csv"
        )
        response.headers["Content-Disposition"] = "attachment; filename=vendas.csv"
        return response

    elif formato == "json":
        return df.to_dict(orient="records")

    else:
        raise HTTPException(status_code=400, detail="Formato não suportado. Use csv ou json.")