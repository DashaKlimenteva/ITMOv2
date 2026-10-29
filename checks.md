# Проверка CLI-генератора отчёта

Фича: CLI-генератор Markdown-отчёта по лабораторной работе
Скрипт: tools/new_lab_report.py
Шаблон: templates/lab_report.md
Контракт: specs/contract.md
Среда: Windows (cmd), Python 3.x

## Таблица проверок

| # | Сценарий | Ожидание | Факт (EXIT) | Статус |
|---|---|---|---|---|
| 1 | Справка (-h) | usage | 0 | ✅ |
| 2 | --lab 3 --fio --group | 0, файл создан, путь в stdout | 0 | ✅ |
| 3 | повтор --lab 3 | 1, файл не перезаписан | 1 | ✅ |
| 4 | --lab abc | 2 | 2 | ✅ |
| 5 | --lab 0 | 2 | 2 | ✅ |
| 6 | --lab 2 --date 2026/10/29 | 2 | 2 | ✅ |
| 7 | нет шаблона (--lab 4) | 1, файл не создан | 1, reports\\lab04.md отсутствует (после удаления старого) | ✅ |
| 8 | --out без --lab | 0, {LAB} сохранён | 0 | ✅ |
| 9 | git status REPORT.md | без изменений | clean | ✅ |

## Доказательства

1. Справка
```
usage: new_lab_report.py [-h] [--lab LAB] [--fio FIO] [--group GROUP]
                         [--date DATE_STR] [--out OUT]
...
EXIT:0
```

2. Успех, путь по умолчанию
```
C:\\DiskZ\\ITMO\\3 semester\\II\\ITMOv2\\reports\\lab03.md
EXIT:0
# ... (контент Markdown созданного отчёта)
```

3. Конфликт файла
```
error: file already exists: reports\\lab03.md
EXIT:1
```

4. --lab не число
```
usage: new_lab_report.py [-h] [--lab LAB] [--fio FIO] [--group GROUP]
                         [--date DATE_STR] [--out OUT]
new_lab_report.py: error: argument --lab: invalid int value: 'abc'
EXIT:2
```

5. --lab < 1
```
error: --lab must be >= 1
EXIT:2
```

6. --date не ISO
```
error: --date must be in format YYYY-MM-DD
EXIT:2
```

7. Нет шаблона
```
error: template not found: templates\\lab_report.md
EXIT:1
MISSING
```

8. --out без --lab
```
C:\\DiskZ\\ITMO\\3 semester\\II\\ITMOv2\\reports\\custom.md
EXIT:0
# ... первая строка содержит {LAB}
```

9. Старые отчёты не изменены
```
On branch p5
nothing to commit, working tree clean
```

## Вывод

Все сценарии соответствуют specs/contract.md.
