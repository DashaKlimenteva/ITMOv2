# Tasks: CLI Markdown Report Generator

- [ ] Шаблон с плейсхолдерами и разделами
- [ ] argparse с --lab/--fio/--group/--date/--out
- [ ] Default path reports/labNN.md (zero-pad 1–9)
- [ ] --lab < 1 → exit 2
- [ ] --date не ISO → exit 2
- [ ] Existing file → exit 1, без перезаписи
- [ ] Missing template → exit 1, файл не создан
- [ ] --out без --lab → exit 0, {LAB} сохранён
- [ ] UTF-8 запись
- [ ] Печать абсолютного пути в stdout
- [ ] Smoke-проверка 9 сценариев из checks.md
