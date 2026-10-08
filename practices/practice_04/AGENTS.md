# AGENTS.md — правила работы в practice_04

## Проект
Учебный сервис подписки Notify Mini. Копия `practices/practice_03/lab/demo` размещена в `practices/practice_04/project/`. Изменения делаем ТОЛЬКО в `project/`.

## Неприкосновенно
- `practices/practice_03/` — сдана, не трогаем.
- `AGENTS.md`, `.opencode/` — инфраструктура агента, менять только по согласованию.

## Стек
- Python 3.10+ (фактически 3.13.5).
- Только стандартная библиотека. Никаких `pip`-зависимостей для `project/`.
- Тесты: `unittest`.
- Нет `make` — runner запускается Python-скриптом.

## Правила кода
- Идентификаторы — на английском. Комментарии — на русском, кратко.
- PEP 8, 4 пробела, длина строки до 100 символов.
- Публичные функции — с docstring.
- Не выдумывать API. Сначала читать существующий код (`service.py`, `test_service.py`) и ссылаться на `file:line` в обсуждениях.

## Workflow при правке
1. Сначала тест (TDD): добавить или обновить тест в `test_service.py`.
2. Затем реализация: изменить `service.py`.
3. Запустить проверку: `python practices/practice_04/runner/run_tests.py`.
4. Если тесты упали — разбираться по трейсам, не гадать. Не «подгонять» тест под неправильный код.
5. Показать diff перед коммитом.

## Runner и hook
- Runner: `python practices/practice_04/runner/run_tests.py`.
- Hook (OpenCode plugin) автоматически запускает runner после правки файла в `project/` и пишет лог в `practices/practice_04/logs/hook.log`.

## Две фичи (A и B)
- A (метрики): `get_subscriber_count()`, `clear_subscribers()`.
- B (нормализация): `normalize_name(name)` + интеграция в `subscribe`.
- Фичи делаются в отдельных worktree (`feature/A-metrics`, `feature/B-normalize`), затем объединяются в `merge/A+B`.

## MCP и skills
- Skill `demo-ci-helper` — оркестрация проверки проекта (запуск runner, краткий отчёт). Рабочая копия: `.opencode/skills/demo-ci-helper/` (видна OpenCode). Дубликат для PR: `practices/practice_04/skills/demo-ci-helper/`. Файлы держим синхронными.
- MCP tool `demo-subscribers` — работа с подписчиками (`count`/`clear`/`add`) с обработкой ошибок. Подключается в корневом `opencode.json` через секцию `mcp` (`type: local`, `command: ["python", "practices/practice_04/mcp/demo-subscribers-tool/server.py"]`).

## Разрешения и поведение агента
- Агенты читают этот файл перед началом работы и следуют правилам.
- Перед изменением файлов в `project/` агент спрашивает подтверждение пользователя (особенно для изменений, влияющих на поведение тестов).
- Разрешено использовать только инструменты, необходимые для разработки: `read`, `grep`, `glob`, `apply_patch`, `bash` (для запуска runner через Python), `skill`, `mcp`.
- Сетевые вызовы запрещены.

## Логи и артефакты
- Логи hook и запусков: `practices/practice_04/logs/`.
- Отчёты скилла и краткие сводки runner: `practices/practice_04/artifacts/`.
- MCP примеры вызовов: `practices/practice_04/mcp/demo-subscribers-tool/examples/`.

## Запрещено
- Сетевые вызовы.
- Установка пакетов без согласования.
- Изменения вне `practices/practice_04/project/` (кроме согласованной инфраструктуры practice_04).
- Удаление тестов и правка их «под код».
