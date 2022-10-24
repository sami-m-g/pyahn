init:
    pip install -r requirements.txt

test:
    python -m coverage run --source=pyahn -m pytest -v tests

coverage:
    python -m coverage report -m

.PHONY: init test coverage