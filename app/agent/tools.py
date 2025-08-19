import httpx, base64, io, pandas as pd, matplotlib.pyplot as plt
from PIL import Image
import pdfplumber

async def web_fetch(url: str, timeout=30) -> dict:
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        r = await client.get(url, headers={"User-Agent": "DataAnalystAgent/1.0"})
    return {"url": str(r.url), "status": r.status_code, "text": r.text}

def html_tables_to_df(html: str) -> list[pd.DataFrame]:
    try:
        return pd.read_html(html)
    except ValueError:
        return []

def pdf_to_text_tables(pdf_bytes: bytes):
    text, tables = "", []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            for table in page.extract_tables() or []:
                tables.append(pd.DataFrame(table))
    return text, tables

def fig_to_data_uri(fig, max_bytes=100_000) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    data = buf.getvalue()
    if len(data) > max_bytes:
        buf2 = io.BytesIO()
        img = Image.open(io.BytesIO(data)).convert("RGB")
        img.save(buf2, format="WEBP", quality=80, method=6)
        data = buf2.getvalue()
        mime = "image/webp"
    else:
        mime = "image/png"
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"

def scatter_with_regression(df: pd.DataFrame, x: str, y: str, dotted_red=False) -> str:
    fig = plt.figure()
    plt.scatter(df[x], df[y])
    m = ((df[x]-df[x].mean())*(df[y]-df[y].mean())).sum() / ((df[x]-df[x].mean())**2).sum()
    b = df[y].mean() - m*df[x].mean()
    xs = pd.Series(sorted(df[x].tolist()))
    ys = m*xs + b
    plt.plot(xs, ys, linestyle="--" if dotted_red else "-")
    plt.xlabel(x); plt.ylabel(y)
    return fig_to_data_uri(fig)
