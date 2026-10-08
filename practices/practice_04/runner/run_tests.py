#!/usr/bin/env python
"""
Lightweight test runner for practices/practice_04/project using unittest.
Runs tests and prints a brief summary; exits with non-zero on failures.
"""
import sys
import pathlib
import unittest


def main() -> int:
    # project_dir: practices/practice_04/project relative to this file
    runner_dir = pathlib.Path(__file__).resolve().parent
    project_dir = runner_dir.parent / "project"

    # Ensure project_dir is importable for `from service import ...`
    sys.path.insert(0, str(project_dir))

    # Discover and run tests
    suite = unittest.defaultTestLoader.discover(start_dir=str(project_dir), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    # Brief summary
    print("\n=== Summary ===")
    print(f"Ran {result.testsRun} tests; Failures: {len(result.failures)}; Errors: {len(result.errors)}")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
