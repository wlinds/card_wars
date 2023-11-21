import importlib
import os
import subprocess
import sys
import time
import unittest


def discover_and_run_tests(test_dir):
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern="*_test.py")

    result = unittest.TextTestRunner().run(suite)

    return result


def main():
    test_dir = "tests"

    # Discover and run tests
    result = discover_and_run_tests(test_dir)

    # Print results
    print(f"\nRan {result.testsRun} tests out of {result.testsRun + len(result.skipped)} modules.")

    if result.errors or result.failures:
        print("The following modules did not run successfully:")
        for error in result.errors + result.failures:
            print(error[0].__module__)


if __name__ == "__main__":
    main()
