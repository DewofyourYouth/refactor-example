import os


def testing():
    os.system("coverage run -m pytest --it --cov=refactor_example")
    os.system("mypy .")


def covhtml():
    os.system("coverage run -m pytest --it --cov=refactor_example --cov-report html")
    os.system("python -m http.server")
