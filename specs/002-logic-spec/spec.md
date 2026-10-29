# Feature Specification: CLI Lab Report Generator

**Feature Branch**: `[not-set]`

**Created**: 2026-10-29

**Status**: Draft

**Input**: User description: "Фича: CLI-генератор Markdown-отчёта по лабораторной работе. Ты — команда логики. Опиши только данные и алгоритм: - входные данные: lab (int ≥ 1), fio, group, date (ISO), out (path); - шаблон: templates/lab_report.md с плейсхолдерами {LAB}, {FIO}, {GROUP}, {DATE}; - алгоритм: загрузка шаблона → выбор пути (default reports/labNN.md с нулём для 1–9, или --out) → проверка существования → mkdir -p → подстановка → запись UTF-8; - правила: если аргумент не передан — плейсхолдер остаётся; если date не передан — системная ISO; - коды возврата: 0 успех, 1 ошибка файла/аргумента/шаблона, 2 argparse; - точный API/CLI-контракт: имена флагов и их типы. Не описывай тексты сообщений для пользователя — это UI."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate report with default path (Priority: P1)

As a user preparing a lab report, I can generate a Markdown file using the standard template and a lab number so that a correctly named file appears in the default reports folder with provided values substituted and missing values left as placeholders.

**Why this priority**: This is the primary flow and enables the core value of producing a usable report artifact quickly.

**Independent Test**: Run the CLI with `--lab 7 --fio "Иванов И.И." --group "K3123"` and without `--out`. Verify a file `reports/lab07.md` is created, the provided fields are substituted, and any omitted fields remain as placeholders.

**Acceptance Scenarios**:

1. Given the template file exists and `--lab 7` is provided, When the CLI runs without `--out`, Then it creates `reports/lab07.md` in UTF-8 and substitutes `{LAB}=7`, plus any provided fields, leaving others unchanged.
2. Given no `--date` is provided, When the CLI runs, Then `{DATE}` is filled with the current system date in ISO (YYYY-MM-DD).

---

### User Story 2 - Generate report to custom path (Priority: P2)

As a user with a custom folder structure, I can specify an explicit output path so that the report is written exactly where I need it regardless of lab number.

**Why this priority**: Supports flexible workflows and integration into existing directories.

**Independent Test**: Run the CLI with `--out docs/labs/lab10.md --fio "Петров П.П." --lab 10`. Verify the file is created at the exact path, intermediate folders are created if needed, and substitutions occur according to rules.

**Acceptance Scenarios**:

1. Given `--out` points to a nested path whose directories do not exist, When the CLI runs, Then the directories are created and the file is written.
2. Given `--out` is provided, When both `--out` and `--lab` are present, Then the output path is taken from `--out` and lab affects only `{LAB}` substitution.

---

### User Story 3 - Handle invalid inputs and errors (Priority: P3)

As a user, I receive a clear outcome code when inputs are invalid or files are missing so that I can automate and diagnose failures.

**Why this priority**: Predictable automation and CI integration require unambiguous exit codes.

**Independent Test**: Provide an invalid `--lab 0` (expect code 2) or a malformed `--date` like `2026/10/29` (expect code 2), or remove the template file (expect code 1). Verify the correct codes are returned and no file is written.

**Acceptance Scenarios**:

1. Given `--lab 0` is provided, When the CLI validates arguments, Then it exits with code 2 (argument parsing error) and does not write any file.
2. Given the template file is missing, When the CLI runs, Then it exits with code 1 (template/file error).

### Edge Cases

- Lab numbers 1–9 map to file names with a leading zero (e.g., `lab01.md`).
- Target output file already exists: abort without writing and return exit code 1.
- Output path not provided and lab not provided: treated as argument parsing error (exit code 2).
- Provided date absent: use current system date in ISO; Provided date present but not ISO: treat as argument parsing error.
  - Date validation enforces the format `YYYY-MM-DD`; invalid formats are treated as argument parsing errors (exit code 2).
- Template readable but lacks expected placeholders: substitute those present; others remain unchanged.

## Requirements *(mandatory)*

### Functional Requirements

- FR-001: The CLI is invoked as `python tools/new_lab_report.py` and exposes the following flags and types:
  - `--lab <int>`: Lab number, integer ≥ 1. Optional unless `--out` is omitted; if `--out` is not provided, `--lab` becomes required to derive the default path. Values < 1 are invalid (argument parsing error).
  - `--fio <string>`: Full name. Optional.
  - `--group <string>`: Group identifier. Optional.
  - `--date <string>`: Date in ISO format (YYYY-MM-DD). Optional. If omitted, the system date in ISO is used for substitution.
  - `--out <path>`: Output file path. Optional. If provided, it overrides the default path.

- FR-002: The template is loaded from `templates/lab_report.md`. Failure to read the template is a runtime error (exit code 1).

- FR-003: Output path resolution:
  - Default path when `--out` is not provided: `reports/labNN.md`, where `NN` is the zero-padded lab number for 1–9, and the non-padded number otherwise (e.g., `lab10.md`).
  - When `--out` is provided: use it verbatim (subject to directory creation and existence checks).
  - If neither `--out` nor a valid `--lab` is provided: treat as argument parsing error (exit code 2).

- FR-4: Existence and directory handling:
  - If the target directory does not exist, create all necessary parent directories before writing.
  - If the target file already exists: do not overwrite; abort with error (exit code 1).

- FR-005: Placeholder substitution rules:
  - Perform textual substitutions on `{LAB}`, `{FIO}`, `{GROUP}`, `{DATE}`.
  - If a corresponding argument is not provided, leave the placeholder unchanged in the output.
  - If `--date` is omitted, substitute `{DATE}` with the current system date in ISO format (YYYY-MM-DD).

- FR-006: File writing uses UTF-8 encoding. Successful completion returns exit code 0.

- FR-007: Error handling and exit codes:
  - Exit code 1: template or file I/O errors, or runtime argument value issues detected after parsing (e.g., unreadable template, write failure).
  - Exit code 2: argument parsing/validation errors (e.g., non-integer lab, lab < 1, malformed date format `YYYY-MM-DD`).
    - `--lab` is not a number or `< 1` → exit code 2.
    - `--date` does not match `YYYY-MM-DD` → exit code 2.

- FR-008: No user-facing text content is specified here; message texts are out of scope for this spec.

### Key Entities *(include if feature involves data)*

- Template: The source Markdown content with placeholders `{LAB}`, `{FIO}`, `{GROUP}`, `{DATE}`.
- CLI Arguments: User-supplied inputs `lab`, `fio`, `group`, `date`, `out`.
- Output Report: The generated Markdown file written to the resolved path.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- SC-001: A user can generate a report via the primary flow (default path) in under 5 seconds from invocation on a typical workstation.
- SC-002: 100% of provided arguments are correctly substituted into the output; omitted arguments leave placeholders unchanged by design.
- SC-003: Zero partial outputs on error: when exit code is non-zero, no new file is created and existing files remain unchanged.
- SC-004: Users can direct output to a custom path successfully on the first attempt at least 95% of the time when the path is valid.

## Assumptions

- The template exists at `templates/lab_report.md` and is readable.
- ISO date is represented as `YYYY-MM-DD` using the system’s local date at execution time when `--date` is omitted.
- Either `--out` is provided or a valid `--lab` is required to derive the default path; if neither is present, this is likely an argument parsing error. [See FR-003]
- Overwrite behavior is defined as aborting without overwriting (exit code 1) to prevent accidental data loss.
 - Коды возврата: 0 — успех, 1 — файл/шаблон/IO, 2 — ошибки аргументов (--lab, --date).
