"""
Descarga una nota (o lista) de Google Keep y la guarda en nota.txt
para que Rainmeter la muestre. Pensado para correr cada pocos minutos.

Requiere:  pip install gkeepapi
Config:    config.json (misma carpeta), ver config.example.json
"""
import json
import traceback
from datetime import datetime
from pathlib import Path

import gkeepapi

BASE = Path(__file__).resolve().parent
OUT = BASE / "nota.txt"
LOG = BASE / "sync.log"


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}\n")


def render(note, show_checked):
    """Convierte la nota en texto plano."""
    if isinstance(note, gkeepapi.node.List):
        lines = []
        for item in note.unchecked:
            sangria = "    " if getattr(item, "indented", False) else ""
            lines.append(f"{sangria}\u2610 {item.text}")  # ☐
        if show_checked:
            for item in note.checked:
                sangria = "    " if getattr(item, "indented", False) else ""
                lines.append(f"{sangria}\u2611 {item.text}")  # ☑
        return "\n".join(lines)
    return note.text or ""


def main():
    cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    email = cfg["email"]
    token = cfg["master_token"]
    title = cfg["note_title"].strip().lower()
    show_checked = cfg.get("show_checked", True)

    keep = gkeepapi.Keep()
    keep.authenticate(email, token)  # descarga todas las notas al autenticar

    elegida = None
    titulos = []
    for n in keep.all():
        if n.trashed:
            continue
        titulos.append(n.title)
        if (n.title or "").strip().lower() == title:
            elegida = n
            break

    if elegida is None:
        log(f"No encontré la nota '{cfg['note_title']}'. Títulos vistos: {titulos}")
        return

    texto = render(elegida, show_checked)
    OUT.write_text(texto, encoding="utf-8")  # UTF-8 sin BOM
    log(f"OK ({len(texto)} caracteres)")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log("ERROR:\n" + traceback.format_exc())
