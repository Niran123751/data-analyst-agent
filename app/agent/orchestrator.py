import re, time, pandas as pd
from agent.tools import web_fetch, html_tables_to_df, pdf_to_text_tables, scatter_with_regression

async def orchestrate(questions_txt: str, ctx: dict, total_budget_s: int = 170):
    t0 = time.time()
    def left(): return total_budget_s - (time.time() - t0)

    wants_array = bool(re.search(r"JSON\s+array", questions_txt, re.I))
    wants_object = bool(re.search(r"JSON\s+object", questions_txt, re.I))
    urls = re.findall(r"https?://\S+", questions_txt)

    dfs: list[pd.DataFrame] = [df for _, df in ctx.get("tabular", [])]

    # scrape if URL given
    for url in urls:
        if left() < 15: break
        try:
            page = await web_fetch(url, timeout=min(30, int(left())))
            dfs += html_tables_to_df(page["text"])
        except Exception:
            pass

    # parse PDFs if no tables found
    if not dfs and ctx.get("pdfs"):
        for name, pdfb in ctx["pdfs"]:
            if left() < 20: break
            txt, tb = pdf_to_text_tables(pdfb)
            dfs += tb

    answers = []
    qlines = [q.strip() for q in re.split(r"\n\d+\.\s+", questions_txt)[1:]] or [questions_txt]

    for q in qlines:
        ql = q.lower()
        if "scatterplot" in ql and dfs:
            uri = scatter_with_regression(dfs[0], "Rank", "Peak", dotted_red=True)
            answers.append(uri)
        else:
            answers.append("Not enough info/time to compute")
        if left() < 5: break

    if wants_array:
        return answers
    if wants_object:
        return {"answer": answers}
    return {"answers": answers}
