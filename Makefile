PYTHON_MODULES := phc
PYTHONPATH := .
VENV := .venv
NOSE := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/nosetests
FLAKE8 := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/flake8
PYTHON := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/python
BLACK := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/black
PDOC := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/pdoc
PRECOMMIT := env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/pre-commit
PIP := $(VENV)/bin/pip3
REQUIREMENTS := -r requirements.txt -r requirements-dev.txt

default: clean test

clean:
	rm -rf build
	rm -rf dist
	rm -rf phc.egg-info

venv: $(VENV)/bin/activate
$(VENV)/bin/activate: requirements-dev.txt
	test -d $(VENV) || virtualenv -p python3 $(VENV)
	$(PIP) install -q $(REQUIREMENTS);
	touch $(VENV)/bin/activate

setup: venv
	$(PRECOMMIT) install

lint: venv
	$(FLAKE8) $(PYTHON_MODULES)

format: venv
	$(BLACK) $(PYTHON_MODULES)

doc: venv
	$(PDOC) --html --output-dir doc/build ./phc --force --config show_inherited_members=True --config list_class_variables_in_index=False --template-dir doc/template

test: lint
	$(NOSE) -v tests

package: venv
	$(PYTHON) setup.py sdist bdist_wheel

deploy: venv
	$(PYTHON) -m twine upload dist/*


.PHONY: default venv requirements bootstrap lint test check package deploy