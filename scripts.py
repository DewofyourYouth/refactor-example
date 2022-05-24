import os


def testing():
    os.system("coverage run -m pytest --it --cov=refactor_example && mypy .")
