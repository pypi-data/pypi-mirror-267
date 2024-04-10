#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "tests.settings.dev")
    settings.PFX_TEST_MODE = True
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests([sys.argv[1:] and sys.argv[1] or "tests"])
    sys.exit(bool(failures))
