init:
    pip install -r requirements.txt

test:
    python -m pytest --cov=pyahn tests

.PHONY: init test