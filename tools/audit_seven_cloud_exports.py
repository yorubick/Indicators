#!/usr/bin/env python3
"""Reproduce the closed-bar comparison from the 2026-10-16 TradingView export.

The TradingView CSV has three adjacent copies of the same 32 study columns:
official study, newly added saved-source copy, and the pre-existing chart copy.
That mapping comes from the controlled chart setup recorded in the audit note;
the CSV header itself repeats names and does not identify studies.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


CURVE_COUNT = 32
BLOCK_STARTS = (5, 5 + CURVE_COUNT, 5 + 2 * CURVE_COUNT)
BLOCK_NAMES = ("official", "newly_added_saved_source", "pre_existing_copy")
R8_E84_OFFSET = 15
DEFAULT_START = datetime(2026, 10, 16, 14, 0, tzinfo=timezone.utc)
DEFAULT_END = datetime(2026, 10, 16, 20, 32, tzinfo=timezone.utc)


def epoch(dt: datetime) -> int:
    return int(dt.timestamp())


def read_export(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        rows = list(reader)
    if len(header) != BLOCK_STARTS[-1] + CURVE_COUNT:
        raise ValueError(f"Expected 101 columns, found {len(header)}")
    blocks = [header[start : start + CURVE_COUNT] for start in BLOCK_STARTS]
    if not (blocks[0] == blocks[1] == blocks[2]):
        raise ValueError("The three 32-column curve headers are not identical")
    return header, rows


def compare(rows: list[list[str]], left: int, right: int) -> dict[str, object]:
    cells = 0
    mismatches = 0
    missing_mismatches = 0
    max_difference = Decimal(0)
    first_mismatch: tuple[str, str, str, str] | None = None
    for row in rows:
        for offset in range(CURVE_COUNT):
            a, b = row[left + offset], row[right + offset]
            if a == "" or b == "":
                if a != b:
                    missing_mismatches += 1
                    mismatches += 1
                    if first_mismatch is None:
                        first_mismatch = (row[0], str(offset), a, b)
                continue
            cells += 1
            difference = abs(Decimal(a) - Decimal(b))
            max_difference = max(max_difference, difference)
            if a != b:
                mismatches += 1
                if first_mismatch is None:
                    first_mismatch = (row[0], str(offset), a, b)
    return {
        "numeric_cells": cells,
        "mismatches": mismatches,
        "missing_pattern_mismatches": missing_mismatches,
        "max_absolute_difference": str(max_difference),
        "first_mismatch": first_mismatch,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path, default=Path(
        "seven_cloud_saved_script_added_2026-10-16_2035UTC.csv"
    ))
    args = parser.parse_args()

    header, all_rows = read_export(args.csv)
    start, end = epoch(DEFAULT_START), epoch(DEFAULT_END)
    closed_rows = [row for row in all_rows if start <= int(row[0]) < end]
    if not closed_rows:
        raise ValueError("No rows found in the documented UTC window")

    first_utc = datetime.fromtimestamp(int(closed_rows[0][0]), timezone.utc)
    last_utc = datetime.fromtimestamp(int(closed_rows[-1][0]), timezone.utc)
    print(f"file: {args.csv}")
    print(f"total_rows: {len(all_rows)}")
    print(f"closed_bar_rows: {len(closed_rows)} ({first_utc.isoformat()} .. {last_utc.isoformat()})")
    print(f"curve_columns_per_study: {CURVE_COUNT}")

    pair_indices = ((BLOCK_STARTS[0], BLOCK_STARTS[1]), (BLOCK_STARTS[0], BLOCK_STARTS[2]))
    for (left, right), right_name in zip(pair_indices, (BLOCK_NAMES[1], BLOCK_NAMES[2])):
        result = compare(closed_rows, left, right)
        print(f"official_vs_{right_name}: {result}")

    print("R8 E84 samples (UTC, official, newly-added, pre-existing):")
    samples = {
        "2026-10-16T14:12:00+00:00",
        "2026-10-16T19:36:00+00:00",
        "2026-10-16T20:31:00+00:00",
        "2026-10-16T20:32:00+00:00",
        "2026-10-16T20:33:00+00:00",
        "2026-10-16T20:34:00+00:00",
    }
    for row in all_rows:
        timestamp = datetime.fromtimestamp(int(row[0]), timezone.utc).isoformat()
        if timestamp in samples:
            values = [row[start + R8_E84_OFFSET] for start in BLOCK_STARTS]
            print(f"  {timestamp}: {', '.join(values)}")


if __name__ == "__main__":
    main()
