# MCP server: demo-subscribers

Stdio MCP сервер для работы с подписчиками (in-memory set).

## Установка в venv

```cmd
python -m venv venv
venv\Scripts\activate
pip install mcp
```

## Запуск вручную

```cmd
venv\Scripts\python practices/practice_04/mcp/demo-subscribers-tool/server.py
```

Ожидается работа по stdio (stdin/stdout); для выхода — Ctrl+C.

## Инструмент

- tool: demo_subscribers (название инструмента — по декоратору @mcp.tool())
- вход: JSON-поля action и опционально name
  - action = count | clear | add
- выход (примерные структуры):
  - count → { "ok": true, "count": N }
  - clear → { "ok": true, "cleared": true }
  - add → { "ok": true, "added": bool, "name": "normalized" }
  - ошибка → { "ok": false, "error": "unknown_action" | "invalid_name" }

## Примеры

См. папку examples/:
- success_count.json — вход/выход для count
- success_add.json — вход/выход для add
- error_unknown_action.json — ошибка для неподдерживаемого действия
- error_invalid_name.json — ошибка для пустого имени

Нормализация имён: trim + collapse spaces + lower.
