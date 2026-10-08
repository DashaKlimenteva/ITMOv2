---
name: demo-ci-helper
description: |
  Оркестрация проверки учебного проекта Notify Mini. Запускает runner
  (python practices/practice_04/runner/run_tests.py), собирает краткий отчёт
  и сохраняет его в practices/practice_04/artifacts/.
  Используй, когда нужно проверить состояние тестов проекта или получить
  сводку по прогону.
---

# Что делает

1. Запускает runner через subprocess.
2. Парсит вывод (Ran N tests, Failures: F, Errors: E).
3. Формирует краткий отчёт по шаблону resources/report_template.md.
4. Сохраняет отчёт в practices/practice_04/artifacts/run_<timestamp>.md.
5. Возвращает агенту краткий текст результата (для отображения).

# Как вызывать

Агент вызывает skill demo-ci-helper в тех случаях, когда нужно:
- проверить, что после правки проекта тесты проходят;
- получить краткую сводку без ручного запуска runner;
- сохранить артефакт прогона в artifacts/.

# Ограничения

- Не модифицирует код проекта.
- Только запускает runner и собирает отчёт.
- Работает только с practices/practice_04/project/.
