.PHONY: docs

install:
	pip install -e . > /dev/null
	pip install -r requirements.txt > /dev/null

sandbox: install
	- rm sandbox/sandbox/db.sqlite3
	sandbox/manage.py syncdb --noinput > /dev/null
	sandbox/manage.py migrate > /dev/null
	sandbox/manage.py loaddata sandbox/fixtures/auth.json page_types > /dev/null

docs:
	$(MAKE) -C docs html
