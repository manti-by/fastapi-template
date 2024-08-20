check:
	git add .
	pre-commit run

test:
	pytest tests/

pip:
	pip install -r requirements.txt

update:
	pcu requirements.txt -u
	pre-commit autoupdate
