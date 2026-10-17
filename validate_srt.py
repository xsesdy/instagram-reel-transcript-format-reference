#!/usr/bin/env python3
"""Check basic SRT cue structure without third-party dependencies."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

STAMP = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$")


def milliseconds(match: re.Match[str], start: int) -> int:
    hours, minutes, seconds, millis = (int(match.group(start + offset)) for offset in range(4))
    return (((hours * 60) + minutes) * 60 + seconds) * 1000 + millis


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip()
    if not text:
        return ["file is empty"]

    errors: list[str] = []
    expected = 1
    for block_number, block in enumerate(re.split(r"\n{2,}", text), start=1):
        lines = block.split("\n")
        if len(lines) < 3:
            errors.append(f"cue {block_number}: needs a number, time range, and text")
            continue
        try:
            cue_number = int(lines[0])
        except ValueError:
            errors.append(f"cue {block_number}: cue number is not an integer")
            continue
        if cue_number != expected:
            errors.append(f"cue {block_number}: expected cue number {expected}, found {cue_number}")
        expected = cue_number + 1
        match = STAMP.fullmatch(lines[1])
        if not match:
            errors.append(f"cue {cue_number}: invalid time range '{lines[1]}'")
        elif milliseconds(match, 1) > milliseconds(match, 5):
            errors.append(f"cue {cue_number}: end time is before start time")
        if not any(line.strip() for line in lines[2:]):
            errors.append(f"cue {cue_number}: missing subtitle text")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate basic SRT cue structure.")
    parser.add_argument("file", type=Path, help="path to an .srt file")
    args = parser.parse_args()
    errors = validate(args.file)
    if errors:
        print("Invalid SRT:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("SRT structure looks valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())