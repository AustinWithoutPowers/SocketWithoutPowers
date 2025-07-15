init: requirements.txt
	pip install -r requirements.txt

test: tests/test_unit_tests.py
	python.exe -m unittest -v tests/test_unit_tests.py

manual_test: tests/manual_test_server.py
	pip install .
	python.exe tests/manual_test_server.py

manual_test_clean: socketwithoutpowers.egg-info
	rd /s /q socketwithoutpowers.egg-info