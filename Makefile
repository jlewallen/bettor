default: checks tests

env:
	python3 -m venv env
	source env/bin/activate && pip3 install -r requirements.txt
	echo
	echo remember to source env/bin/activate
	echo

checks: env
	env/bin/mypy server/*.py --ignore-missing-imports

tests: env
	rm -f test*.sqlite3
	env/bin/python3 -m pytest server/test_*.py

update-test: env
	rm -f test*.sqlite3
	env/bin/python3 -m pytest server/test_*.py --snapshot-update

wipe:
	rm -rf server/snapshots

image:
	docker build -t jlewallen/bettor .
