# ReAct

- Цель: создать practices/practice_02/react/tests_load_improved.md и заполнить practices/practice_02/react/experiment.md на основе указанных источников.
- Доступные входы: practices/practice_01/CASE.md; practices/practice_01/problem.md; practices/practice_01/TRAINING_PR.diff (app/api.py:35-38; app/review_service.py:19-22); practices/practice_01/tests_load.md (L1-L3 и evidence).
- Разрешённые действия: читать источники; извлекать правила API-1, REL-1, QA-1, OBS-1; извлекать метрики; извлекать строки диффа; создавать tests_load_improved.md; заполнять experiment.md.
- Запрещённые действия: менять practices/practice_01/tests_load.md; использовать знания вне источников; выдумывать пороги и кейсы; логировать diff; p99 вместо p95; писать «возможно».
- Максимальное число шагов: 6.
- Условие остановки и вопроса человеку: если в источниках нет нужного правила, метрики или строки diff — остановиться и спросить.

## Запрос

Собрать улучшенные нагрузочные тесты, перенося только подтверждённые кейсы (правилом или строкой diff), указать пороги, инструменты, критерии провала, связь с метриками и evidence. Источники: CASE.md (API-1, REL-1, QA-1, OBS-1), problem.md (метрики), TRAINING_PR.diff (app/api.py:35-38; app/review_service.py:19-22), tests_load.md (L1-L3). Не менять исходный tests_load.md.
## Наблюдаемые действия и результаты

| Шаг | Действие | Наблюдение | Решение продолжить или остановиться |
|---|---|---|---|
| 1 | Thought: прочитать CASE.md и зафиксировать правила API-1, REL-1, QA-1, OBS-1 | API-1: 20000 символов → 413; REL-1: таймаут 10 секунд → контролируемый ответ; QA-1 подтверждение рисков; OBS-1 логирование без содержимого | Continue |
| 2 | Thought: прочитать problem.md и извлечь метрики | Найдена метрика «Доля 5xx на POST /api/reviews < 1%» | Continue |
| 3 | Thought: прочитать TRAINING_PR.diff и найти нужные строки | app/api.py:35-38 (эндпоинт), app/review_service.py:19-22 (вызов LLM) | Continue |
| 4 | Thought: прочитать tests_load.md и оценить L1-L3 и evidence | L1 подтверждён API-1; L3 подтверждён REL-1; L2 не подтверждён правилом/диффом | Continue |
| 5 | Action: создать tests_load_improved.md с L1 и L3; для каждого указать пороги, инструменты, критерии провала, связь с метриками и evidence | Файл создан: L1 (API-1 + строки diff), L3 (REL-1/OBS-1 + строки diff) | Continue |
| 6 | Observation: проверить соответствие ограничениям (не меняли tests_load.md; нет выдуманных порогов; нет p99; не логируем diff) | Условия соблюдены; все пороги из источников; L2 исключён | Stop |

## Что изменили в исходном артефакте

- Файл и раздел: practices/practice_02/react/tests_load_improved.md — весь документ.
- Изменение: добавлены подтверждённые пороги (20000 символов; 10 секунд), инструменты, критерии провала, связь с метриками и evidence; исключён L2 как неподтверждённый.
- Как проверили: сопоставили с CASE.md (API-1, REL-1, QA-1, OBS-1), problem.md (метрики), TRAINING_PR.diff (app/api.py:35-38; app/review_service.py:19-22), tests_load.md (L1-L3 и evidence).
- Что отклонили: L2; любые SLO по латентности; p99; любые данные вне источников; логирование diff.
