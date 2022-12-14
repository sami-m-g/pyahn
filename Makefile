init:
    pip install -r requirements.txt

lint:
	python -m flake8 --max-line-length 150

test:
    python -m coverage run --source=pyahn -m pytest -v tests

coverage:
    python -m coverage report -m

run:
    python -m pyahn.core -i data/ellipsis_sample.csv

.PHONY: init test coverage run