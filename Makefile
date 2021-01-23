default: checks tests

env:
	python3 -m venv env
	echo REMEMBER TO DO THIS
	echo source env/bin/activate
	echo pip3 install -r requirements.txt

src/config.ts: src/config.ts.dev
	cp src/config.ts.dev src/config.ts

setup: env src/config.ts

checks: setup
	env/bin/mypy server/*.py --ignore-missing-imports

tests: setup
	rm -f test*.sqlite3
	env/bin/python3 -m pytest server/test_*.py

update-test: setup
	rm -f test*.sqlite3
	env/bin/python3 -m pytest server/test_*.py --snapshot-update

wipe:
	rm -rf server/snapshots

image:
	docker build -t jlewallen/bettor .

prod-image:
	cp src/config.ts.prod src/config.ts
	docker build -t jlewallen/bettor .
