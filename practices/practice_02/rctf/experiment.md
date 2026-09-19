# R.C.T.F.

- **Role:** Технический аналитик, архитектор и AI-ревьюер.
- **Context:** practices/practice_01/tests_load.md (только чтение), practices/practice_01/CASE.md (API-1, REL-1, QA-1, OBS-1), practices/practice_01/problem.md (метрики), practices/practice_01/TRAINING_PR.diff (app/api.py:35-38; app/review_service.py:19-22).
- **Task:** создать practices/practice_02/rctf/tests_load_improved.md и заполнить practices/practice_02/rctf/experiment.md. Переносить только кейсы, подтверждённые правилом или строкой диффа; указать пороги, инструменты, критерии провала, связь с метриками и evidence.
- **Format:** ответ из двух частей (полные файлы tests_load_improved.md и experiment.md). Исходный tests_load.md не менять.

## Полный запрос

Собрать улучшенные нагрузочные тесты на основе CASE.md (API-1, REL-1, QA-1, OBS-1), problem.md (метрики) и TRAINING_PR.diff (app/api.py:35-38; app/review_service.py:19-22). Переносить только подтверждённые кейсы. Указать пороги из источников, инструменты, критерии провала, связь с метриками и evidence. Не логировать diff. Не добавлять p99, не писать «возможно».
## Что получили

Создан файл practices/practice_02/rctf/tests_load_improved.md с кейсами L1 и L3 (подтверждены правилами/диффом). L2 не перенесён как неподтверждённый правилом или строкой диффа.
## Что изменили в исходном артефакте

- Файл и раздел: practices/practice_02/rctf/tests_load_improved.md — весь документ.
- Изменение: добавлены подтверждённые пороги (20000 символов по API-1, 10 секунд по REL-1), инструменты, критерии провала, связь с метриками и evidence на кейс.
- Как проверили: сверили с CASE.md (API-1, REL-1, QA-1, OBS-1), problem.md (таблица метрик «Доля 5xx < 1%»), TRAINING_PR.diff (app/api.py:35-38; app/review_service.py:19-22), practices/practice_01/tests_load.md (L1-L3).
- Что отклонили: L2 (параллельность) как неподтверждённый правилом/диффом; любые SLO по латентности; p99; любые числа не из источников.
