import pandas as pd

def load_excel(path: str) -> list[dict]:
    df = pd.read_excel(path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    required_columns = {"setor", "tipo"}

    if not required_columns.issubset(set(df.columns)):
        raise Exception(
            f"Excel must contain columns: {required_columns}. Found: {list(df.columns)}"
        )

    df["tipo"] = df["tipo"].astype(str).str.lower().str.strip()
    df["setor"] = df["setor"].astype(str).str.strip()

    return df.to_dict(orient="records")