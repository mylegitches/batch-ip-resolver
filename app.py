from __future__ import annotations

from datetime import datetime
from io import StringIO
import os
from typing import Iterable, List, Tuple

from flask import Flask, Response, render_template, request

from ip_resolver import resolve_ip


app = Flask(__name__)


def parse_domains(multiline_text: str, uploaded_text: str | None) -> List[str]:
    combined_text = "\n".join(
        part for part in [multiline_text or "", uploaded_text or ""] if part
    )
    lines = [line.strip() for line in combined_text.splitlines()]
    non_empty = [line for line in lines if line]
    deduped_preserving_order = list(dict.fromkeys(non_empty))
    return deduped_preserving_order


def create_tsv(rows: Iterable[Tuple[str, str]]) -> str:
    buffer = StringIO()
    buffer.write("URL\tIP Address\n")
    for url, ip in rows:
        buffer.write(f"{url}\t{ip}\n")
    return buffer.getvalue()


@app.get("/")
def index() -> str:
    return render_template("index.html", results=None, submitted_text="")


@app.post("/resolve")
def resolve() -> Response | str:
    textarea_text = request.form.get("domains", "")

    uploaded_text: str | None = None
    uploaded_file = request.files.get("file")
    if uploaded_file and uploaded_file.filename:
        uploaded_bytes = uploaded_file.stream.read()
        uploaded_text = uploaded_bytes.decode("utf-8", errors="ignore")

    domains = parse_domains(textarea_text, uploaded_text)
    results: List[Tuple[str, str]] = [(domain, resolve_ip(domain)) for domain in domains]

    if request.form.get("download") == "tsv":
        tsv_content = create_tsv(results)
        stamp = datetime.now().strftime("%Y%m%d")
        filename = f"results_{stamp}.tsv"
        return Response(
            tsv_content,
            mimetype="text/tab-separated-values",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
            },
        )

    submitted_text = "\n".join(domains)
    return render_template("index.html", results=results, submitted_text=submitted_text)


if __name__ == "__main__":
    port_env = os.environ.get("PORT", "5000")
    try:
        port = int(port_env)
    except ValueError:
        port = 5000
    debug_flag = os.environ.get("DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host="0.0.0.0", port=port, debug=debug_flag)


