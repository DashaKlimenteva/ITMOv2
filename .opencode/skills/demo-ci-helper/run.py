#!/usr/bin/env python
import sys
import subprocess
import pathlib
import datetime as dt


def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parents[3]
    runner = repo_root / "practices" / "practice_04" / "runner" / "run_tests.py"
    artifacts_dir = repo_root / "practices" / "practice_04" / "artifacts"
    template_path = pathlib.Path(__file__).resolve().parent / "resources" / "report_template.md"

    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # Run runner and capture stdout
    proc = subprocess.run([sys.executable, str(runner)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = proc.stdout

    # Parse summary line: "=== Summary ===\nRan N tests; Failures: F; Errors: E"
    total = failures = errors = 0
    for line in output.splitlines():
        if line.strip().startswith("Ran ") and ";" in line:
            try:
                # Example: Ran 3 tests; Failures: 0; Errors: 0
                parts = [p.strip() for p in line.split(';')]
                # Ran N tests
                total = int(parts[0].split()[1])
                # Failures: F
                failures = int(parts[1].split(':')[1].strip())
                # Errors: E
                errors = int(parts[2].split(':')[1].strip())
            except Exception:
                pass

    passed = max(total - failures - errors, 0)
    status = "OK" if proc.returncode == 0 else "FAIL"

    # Load template
    template = template_path.read_text(encoding="utf-8")
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    report = (
        template
        .replace("{{timestamp}}", ts)
        .replace("{{total}}", str(total))
        .replace("{{passed}}", str(passed))
        .replace("{{failures}}", str(failures))
        .replace("{{errors}}", str(errors))
        .replace("{{status}}", status)
    )

    # Write artifact
    artifact_path = artifacts_dir / f"run_{ts}.md"
    artifact_path.write_text(report, encoding="utf-8")

    # Print brief summary to stdout
    print(f"Tests: {total}, Passed: {passed}, Failures: {failures}, Errors: {errors}, Status: {status}")
    return 0 if proc.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
