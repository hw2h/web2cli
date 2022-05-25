pytest: # run tests
	pytest -vvvvv tests/

run: # run application
	export PYTHONPATH=. && python app/server.py
