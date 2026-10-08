#!/usr/bin/env python
import sys
import subprocess
import pathlib
import datetime as dt


def main() -> int:
    # Directly resolve practice_04 directory relative to this file
    # practice_04 directory (two levels up from this file):
    # practices/practice_04/skills/demo-ci-helper/run.py -> parents[2] = practices/practice_04
    practice04_dir = pathlib.Path(__file__).resolve().parents[2]
    runner = practice04_dir / "runner" / "run_tests.py"
    artifacts_dir = practice04_dir / "artifacts"
    template_path = pathlib.Path(__file__).resolve().parent / "resources" / "report_template.md"

    artifacts_dir.mkdir(parents=True, exist_ok=True)

    proc = subprocess.run([sys.executable, str(runner)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = proc.stdout
    # Debug: print runner output for verification in this practice
    print(output)

    total = failures = errors = 0
    for line in output.splitlines():
        if line.strip().startswith("Ran ") and ";" in line:
            try:
                parts = [p.strip() for p in line.split(';')]
                total = int(parts[0].split()[1])
                failures = int(parts[1].split(':')[1].strip())
                errors = int(parts[2].split(':')[1].strip())
            except Exception:
                pass

    passed = max(total - failures - errors, 0)
    status = "OK" if proc.returncode == 0 else "FAIL"

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

    artifact_path = artifacts_dir / f"run_{ts}.md"
    artifact_path.write_text(report, encoding="utf-8")

    print(f"Tests: {total}, Passed: {passed}, Failures: {failures}, Errors: {errors}, Status: {status}")
    return 0 if proc.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
