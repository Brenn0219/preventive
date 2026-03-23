import pandas as pd

def load_excel(path):
    df = pd.read_excel(path)

    if "setor" not in df.columns or "tipo" not in df.columns:
        raise Exception("Excel deve ter colunas: setor, tipo")

    df["tipo"] = df["tipo"].astype(str).str.lower().str.strip()
    df["setor"] = df["setor"].astype(str).str.strip()

    return df.to_dict(orient="records")