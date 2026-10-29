#!/usr/bin/env python3
"""
CLI: Generate a Markdown lab report from an external template.

Contract:
- Default output: reports/labNN.md when --out not given
- Existing file -> exit code 1 (no overwrite)
- Missing template -> exit code 1
- --lab < 1 -> exit code 2
- --date not in YYYY-MM-DD -> exit code 2

User-facing messages are in Russian as per UI contract.
"""

import argparse
import sys
from pathlib import Path
from datetime import date


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Генератор Markdown-отчёта по лабораторной работе из шаблона",
    )
    parser.add_argument("--lab", type=int, help="Номер лабораторной (обязателен, если не указан --out)")
    parser.add_argument("--fio", type=str, help="ФИО для подстановки в {FIO}")
    parser.add_argument("--group", type=str, help="Группа для подстановки в {GROUP}")
    parser.add_argument(
        "--date", dest="date_str", type=str, help="Дата для {DATE} (формат YYYY-MM-DD)"
    )
    parser.add_argument(
        "--out", type=Path, help="Путь к выходному файлу (по умолчанию reports/labNN.md)"
    )
    args = parser.parse_args(argv)

    # Требование контракта: --lab обязателен, если не задан --out
    if args.out is None and args.lab is None:
        sys.stderr.write("Ошибка: флаг --lab обязателен, если не указан --out\n")
        sys.exit(2)

    # Требование контракта: --lab < 1 -> код 2
    if args.lab is not None and args.lab < 1:
        sys.stderr.write("Ошибка: --lab должен быть >= 1\n")
        sys.exit(2)

    # Требование контракта: --date не в формате YYYY-MM-DD -> код 2
    if args.date_str:
        try:
            date.fromisoformat(args.date_str)
        except ValueError:
            sys.stderr.write("Ошибка: --date должен быть в формате YYYY-MM-DD\n")
            sys.exit(2)
    return args


def default_output_path(lab: int) -> Path:
    nn = f"{lab:02d}" if lab < 10 else str(lab)
    return Path("reports") / f"lab{nn}.md"


def load_template(template_path: Path) -> str:
    if not template_path.exists():
        # Требование контракта: нет шаблона -> код 1
        sys.stderr.write(f"Ошибка: шаблон не найден: {template_path}\n")
        sys.exit(1)
    return template_path.read_text(encoding="utf-8")


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)

    template_path = Path("templates") / "lab_report.md"
    content = load_template(template_path)

    # Выбор выходного пути
    if args.out is not None:
        out_path = args.out
    else:
        out_path = default_output_path(args.lab)

    # Не перезаписывать существующий файл: код 1
    if out_path.exists():
        sys.stderr.write(f"Ошибка: файл уже существует: {out_path}\n")
        return 1

    # Создать директории при необходимости
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Подстановки: DATE по умолчанию сегодня, остальные — если переданы
    lab_value = str(args.lab) if args.lab is not None else None
    date_value = args.date_str if args.date_str else date.today().isoformat()
    fio_value = args.fio
    group_value = args.group

    if lab_value is not None:
        content = content.replace("{LAB}", lab_value)
    content = content.replace("{DATE}", date_value)
    if fio_value is not None:
        content = content.replace("{FIO}", fio_value)
    if group_value is not None:
        content = content.replace("{GROUP}", group_value)

    out_path.write_text(content, encoding="utf-8")
    # Успех: печать абсолютного пути и код 0
    print(str(out_path.resolve()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
