check:
	git add .
	pre-commit run

test:
	pytest -W ignore::DeprecationWarning tests/

pip:
	pip install -r requirements.txt

update:
	pcu requirements.txt -u
	pre-commit autoupdate

migrate:
	alembic upgrade head