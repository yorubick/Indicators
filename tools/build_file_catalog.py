#!/usr/bin/env python3
"""Build a SHA-256 inventory for the PoiSzn research folder."""
from __future__ import annotations

import csv
import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "FILE_CATALOG.csv"
EXCLUDED_DIRS = {".git", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
CHUNK_SIZE = 1024 * 1024


def category(relative: str) -> str:
    parts = Path(relative).parts
    suffix = Path(relative).suffix.lower()
    if parts[0] == "manual":
        return "tradingview_manual_evidence"
    if parts[0] == "imports":
        return "imported_source"
    if parts[0] == "docs":
        return "project_documentation"
    if parts[0] == "tools":
        return "maintenance_tool"
    if suffix in {".py", ".pine", ".ps1", ".sh"}:
        return "source_code"
    if suffix in {".json", ".csv", ".tsv", ".xlsx"}:
        return "dataset_or_analysis_output"
    if suffix in {".md", ".txt", ".pdf"}:
        return "historical_documentation"
    return "other_project_file"


def files_under_root():
    for directory, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS)
        for filename in sorted(filenames):
            path = Path(directory) / filename
            if path in {OUTPUT, OUTPUT.with_suffix(".csv.tmp")} or path.suffix.lower() in EXCLUDED_SUFFIXES or path.is_symlink():
                continue
            yield path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(CHUNK_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    temporary = OUTPUT.with_suffix(".csv.tmp")
    count = 0
    total = 0
    try:
        with temporary.open("w", newline="", encoding="utf-8-sig") as stream:
            writer = csv.writer(stream)
            writer.writerow(("relative_path", "category", "bytes", "sha256"))
            for path in files_under_root():
                relative = path.relative_to(ROOT).as_posix()
                size = path.stat().st_size
                writer.writerow((relative, category(relative), size, sha256(path)))
                count += 1
                total += size
                if count % 250 == 0:
                    print(f"hashed {count} files ({total:,} bytes)", flush=True)
        temporary.replace(OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()
    print(f"catalog={OUTPUT}")
    print(f"files={count}; bytes={total:,}")


if __name__ == "__main__":
    main()

