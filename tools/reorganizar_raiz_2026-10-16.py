"""Reorganización de la raíz del 16-oct-2026 (fase A: informes, Pine y medios).

Mueve con `git mv`:
  *.md (salvo README.md)           -> reports/
  *.pine                           -> pine/
  *.jpg, *.png, *.svg              -> media/
  *_audio.wav y *_transcripcion*   -> media/audio/

Después reescribe las referencias:
  - Enlaces Markdown relativos (y rutas G:/trading/guias/analisis/...) en los
    .md del proyecto, recalculados desde la nueva ubicación de cada documento.
  - Literales de nombre de archivo en los .py de la raíz, tools/ y experimentos/.

No modifica el contenido de imports/, manual/ ni de los archivos *recibido*
(instantáneas cuyo SHA-256 está registrado en las auditorías).

Los scripts .py y los datos .json/.csv de la raíz NO se mueven: están acoplados
mediante ROOT = Path(__file__).parent, imports entre módulos y nombres
dinámicos. Ver docs/PROJECT_MAP.md.

Uso:  python tools/reorganizar_raiz_2026-10-16.py [--apply]
Escribe la tabla de correspondencias en docs/REORGANIZACION_2026-10-16.csv.
"""
from __future__ import annotations

import csv
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[1]
APPLY = "--apply" in sys.argv
OLD_PREFIXES = ("file:///G:/trading/guias/analisis/", "G:/trading/guias/analisis/")
SKIP_DIRS = {".git", "imports", "manual"}


def destination(name: str) -> str | None:
    lower = name.lower()
    if name == "README.md":
        return None
    if lower.endswith("_audio.wav") or "_transcripcion" in lower:
        return "media/audio"
    if lower.endswith(".md"):
        return "reports"
    if lower.endswith(".pine"):
        return "pine"
    if lower.endswith((".jpg", ".png", ".svg")):
        return "media"
    return None


def build_mapping() -> dict[str, str]:
    mapping = {}
    for path in sorted(ROOT.iterdir()):
        if path.is_file():
            folder = destination(path.name)
            if folder:
                mapping[path.name] = f"{folder}/{path.name}"
    return mapping


def is_frozen(rel: str) -> bool:
    parts = Path(rel).parts
    return parts[0] in SKIP_DIRS or "recibido" in Path(rel).name.lower()


LINK = re.compile(r'(\]\(\s*<?)([^)\s>]+)(>?(?:\s+"[^"]*")?\s*\))|(<img[^>]+src=")([^"]+)(")')


def rewrite_markdown(text: str, old_rel: str, new_rel: str, mapping: dict[str, str]) -> str:
    old_dir = (ROOT / old_rel).parent
    new_dir = (ROOT / new_rel).parent

    def fix(target: str) -> str:
        if re.match(r"^(https?:|mailto:|#)", target):
            return target
        path_part, sep, anchor = target.partition("#")
        decoded = unquote(path_part)
        if not decoded:
            return target
        absolute = None
        for prefix in OLD_PREFIXES:
            if decoded.startswith(prefix):
                absolute = ROOT / decoded[len(prefix):]
                break
        if absolute is None:
            if decoded.startswith("file:///") or re.match(r"^[A-Za-z]:[\\/]", decoded):
                return target  # ruta absoluta ajena al proyecto: se deja igual
            absolute = (old_dir / decoded).resolve()
        try:
            rel_old = absolute.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            return target
        rel_new = mapping.get(rel_old, rel_old)
        if not (ROOT / rel_new).exists() and not (ROOT / rel_old).exists():
            return target  # enlace ya roto: no se inventa destino
        link = os.path.relpath(ROOT / rel_new, new_dir).replace(os.sep, "/")
        link = quote(link, safe="/._-~()")
        return link + (sep + anchor if sep else "")

    def repl(match: re.Match) -> str:
        if match.group(2) is not None:
            return match.group(1) + fix(match.group(2)) + match.group(3)
        return match.group(4) + fix(match.group(5)) + match.group(6)

    return LINK.sub(repl, text)


def rewrite_python(text: str, mapping: dict[str, str]) -> str:
    for name, new in mapping.items():
        escaped = re.escape(name)
        # 'nombre' o "nombre" exactos
        text = re.sub(rf"(['\"]){escaped}(['\"])", rf"\g<1>{new}\g<2>", text)
        # rutas absolutas del equipo original
        text = text.replace(f"G:\\trading\\guias\\analisis\\{name}",
                            "G:\\trading\\guias\\analisis\\" + new.replace("/", "\\"))
        text = text.replace(f"G:/trading/guias/analisis/{name}", f"G:/trading/guias/analisis/{new}")
    return text


def main() -> None:
    mapping = build_mapping()
    # Archivos de texto del proyecto, con su ruta antes y después del movimiento.
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if is_frozen(rel) or path.suffix not in (".md", ".py"):
            continue
        if rel == "tools/reorganizar_raiz_2026-10-16.py":
            continue
        files.append((rel, mapping.get(rel, rel)))

    changes = {}
    for old_rel, new_rel in files:
        text = (ROOT / old_rel).read_text(encoding="utf-8")
        if old_rel.endswith(".md"):
            new_text = rewrite_markdown(text, old_rel, new_rel, mapping)
        else:
            new_text = rewrite_python(text, mapping)
        if new_text != text:
            changes[old_rel] = (new_rel, new_text)

    print(f"archivos a mover: {len(mapping)}")
    for folder in sorted({v.rsplit('/', 1)[0] for v in mapping.values()}):
        print(f"  {folder}/: {sum(v.startswith(folder + '/') and v.count('/') == folder.count('/') + 1 for v in mapping.values())}")
    print(f"archivos con referencias reescritas: {len(changes)}")
    for old_rel in sorted(changes):
        print("  ", old_rel)
    if not APPLY:
        print("(simulación; use --apply para ejecutar)")
        return

    for old, new in mapping.items():
        (ROOT / new).parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "mv", old, new], cwd=ROOT, check=True)
    for _, (new_rel, new_text) in changes.items():
        with open(ROOT / new_rel, "w", encoding="utf-8", newline="") as handle:
            handle.write(new_text)

    table = ROOT / "docs" / "REORGANIZACION_2026-10-16.csv"
    with table.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["ruta_anterior", "ruta_nueva"])
        writer.writerows(sorted(mapping.items()))
    print(f"tabla: {table.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
