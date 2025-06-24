import pandas as pd
import io

def processar_csv(arquivo_csv: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(arquivo_csv.decode('utf-8')))
    df = df.dropna()
    df = df.drop_duplicates()
    df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
    df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df = df[df['preco'] > 0]
    df = df[df['quantidade'] > 0]
    return df
