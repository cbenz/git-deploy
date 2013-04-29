.PHONY: clean flake8 tests

all: clean flake8 tests

clean:
	find -name "*.pyc" | xargs rm -f

flake8:
	flake8 --max-line-length=120 --ignore=E123,E128 git_deploy scripts/*

tests:
	nosetests
