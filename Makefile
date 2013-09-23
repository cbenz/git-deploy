.PHONY: clean flake8 tests

all: clean flake8 tests

clean:
	find -name "*.pyc" | xargs rm -f

flake8:
    # E123 Closing bracket does not match indentation of opening bracket's line
    # H701 Empty localization string
    # H803 Commit message should not end with a period
    # The find command is a hack to avoid a python-hacking bug.(exception with empty __init__.py files).
	find git_deploy -type f -name '*.py' -size +0 | xargs flake8 --max-line-length=120 --ignore=E123,H701,H803

tests:
	python -m unittest discover
