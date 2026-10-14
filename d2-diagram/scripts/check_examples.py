#!/usr/bin/env python3
"""Compile every Markdown D2 example; retain source and SVG files for review."""

import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    compiler = shutil.which("d2")
    if compiler is None:
        parser.error("d2 is not installed or is not on PATH")
    root = Path(__file__).resolve().parents[1]
    output = args.output_dir.resolve()
    if output == root or root in output.parents:
        parser.error("use an output directory outside the installed skill")
    output.mkdir(parents=True, exist_ok=True)
    version = subprocess.run([compiler, "--version"], capture_output=True, text=True, check=True)
    print(version.stdout.strip())
    count = 0
    failures = 0
    for document in sorted(root.rglob("*.md")):
        source = document.read_text(encoding="utf-8")
        for index, match in enumerate(re.finditer(r"^```d2\s*\n(.*?)^```\s*$", source, re.M | re.S), 1):
            count += 1
            relative = document.relative_to(root)
            label = f"{relative}:{source.count(chr(10), 0, match.start()) + 1}"
            stem = "--".join(relative.with_suffix("").parts) + f"--{index}"
            diagram = output / f"{stem}.d2"
            diagram.write_text(match.group(1), encoding="utf-8")
            svg = diagram.with_suffix(".svg")
            # Remove a previous result so failure cannot leave a misleading SVG.
            svg.unlink(missing_ok=True)
            try:
                result = subprocess.run(
                    [compiler, "--timeout", "25", str(diagram), str(svg)],
                    capture_output=True, text=True, timeout=30,
                )
            except subprocess.TimeoutExpired:
                failures += 1
                print(f"FAIL {label}: compilation timed out", file=sys.stderr)
                continue
            if result.returncode or not svg.is_file() or not svg.stat().st_size:
                failures += 1
                print(f"FAIL {label}\n{result.stderr}", file=sys.stderr)
            else:
                print(f"PASS {label}")
    print(f"{count - failures}/{count} examples compiled; visual review is still required.")
    return 1 if failures or count == 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
