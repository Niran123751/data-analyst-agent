import pandas as pd, io, json
from fastapi import UploadFile

async def load_attachments(files):
    out = {"tabular": [], "text": [], "pdfs": [], "images": [], "raw": []}
    for f in files:
        data = await f.read()
        name = f.filename.lower()
        try:
            if name.endswith(".csv"):
                out["tabular"].append((name, pd.read_csv(io.BytesIO(data))))
            elif name.endswith((".xlsx", ".xls")):
                out["tabular"].append((name, pd.read_excel(io.BytesIO(data))))
            elif name.endswith(".json"):
                out["text"].append((name, json.loads(data.decode("utf-8", "ignore"))))
            elif name.endswith(".parquet"):
                out["tabular"].append((name, pd.read_parquet(io.BytesIO(data))))
            elif name.endswith(".pdf"):
                out["pdfs"].append((name, data))
            elif name.endswith((".png",".jpg",".jpeg",".webp")):
                out["images"].append((name, data))
            else:
                out["raw"].append((name, data))
        except Exception:
            out["raw"].append((name, data))
    return out
