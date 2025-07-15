init:
	pip install -r requirements.txt

test:
	python.exe -m unittest -v tests/test_unit_tests.py