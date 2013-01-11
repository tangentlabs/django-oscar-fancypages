.PHONY: docs

install:
	python setup.py develop > /dev/null
	pip install -r requirements.txt > /dev/null

sandbox: install
	- rm sandbox/sandbox/db.sqlite3
	sandbox/manage.py syncdb --noinput > /dev/null
	sandbox/manage.py migrate > /dev/null
	#sandbox/manage.py loaddata sandbox/fixtures/auth.json sandbox/fixtures/fancypages.json > /dev/null

docs:
	$(MAKE) -C docs html
