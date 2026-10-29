#!/usr/bin/env python3
"""
CLI: Generate a Markdown lab report from an external template (Practice 05 scope).
Default locations are scoped to practices/practice_05/.

Behavior:
- Default output: practices/practice_05/reports/labNN.md (zero-padded 1-9) when --out not given
- Do not overwrite existing files (stderr + exit code 1)
- Placeholders in template: {LAB}, {FIO}, {GROUP}, {DATE}
  - If an argument is not provided, placeholder remains as-is
  - For DATE: if --date not provided, use today's ISO date (YYYY-MM-DD)
- Cross-platform paths via pathlib; create parent dirs as needed
"""

import argparse
import sys
from pathlib import Path
from datetime import date


def base_dir() -> Path:
    # File is located at practices/practice_05/tools/new_lab_report.py
    # Base directory for templates/reports is practices/practice_05/
    return Path(__file__).resolve().parents[1]


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Generate a Markdown lab report from a template (practice_05)",
    )
    parser.add_argument("--lab", type=int, help="Lab number (required if --out not given)")
    parser.add_argument("--fio", type=str, help="Full name for {FIO}")
    parser.add_argument("--group", type=str, help="Group for {GROUP}")
    parser.add_argument("--date", dest="date_str", type=str, help="Date for {DATE} (ISO YYYY-MM-DD)")
    parser.add_argument("--out", type=Path, help="Output path (overrides default practices/practice_05/reports/labNN.md)")
    args = parser.parse_args(argv)

    # Validate presence of --lab when --out is not provided
    if args.out is None and args.lab is None:
        sys.stderr.write("error: --lab is required when --out is not provided\n")
        sys.exit(1)
    return args


def default_output_path(lab: int) -> Path:
    # Zero-pad 1..9; otherwise as-is
    nn = f"{lab:02d}" if lab < 10 else str(lab)
    return base_dir() / "reports" / f"lab{nn}.md"


def template_path() -> Path:
    return base_dir() / "templates" / "lab_report.md"


def load_template(path: Path) -> str:
    if not path.exists():
        sys.stderr.write(f"error: template not found: {path}\n")
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)

    content = load_template(template_path())

    # Decide output path
    if args.out is not None:
        out_path = args.out
    else:
        out_path = default_output_path(args.lab)

    # Refuse to overwrite
    if out_path.exists():
        sys.stderr.write(f"error: file already exists: {out_path}\n")
        return 1

    # Ensure parent directories
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Prepare substitutions: only replace provided args; DATE uses default if missing
    lab_value = str(args.lab) if args.lab is not None else None
    date_value = args.date_str if args.date_str else date.today().isoformat()
    fio_value = args.fio
    group_value = args.group

    # Apply replacements selectively
    if lab_value is not None:
        content = content.replace("{LAB}", lab_value)
    content = content.replace("{DATE}", date_value)
    if fio_value is not None:
        content = content.replace("{FIO}", fio_value)
    if group_value is not None:
        content = content.replace("{GROUP}", group_value)

    # Write output
    out_path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
