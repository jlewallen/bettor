default: checks tests

env:
	python3 -m venv env
	echo REMEMBER TO DO THIS
	echo source env/bin/activate
	echo pip3 install -r req.txt

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

vapid:
	openssl ecparam -name prime256v1 -genkey -noout -out vapid_private.pem
	openssl ec -in ./vapid_private.pem -outform DER|tail -c +8|head -c 32|base64|tr -d '=' |tr '/+' '_-' >> private_key.txt
	openssl ec -in ./vapid_private.pem -pubout -outform DER|tail -c 65|base64|tr -d '=' |tr '/+' '_-' >> public_key.txt
