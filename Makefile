VENV = ./activate_venv

venv: 
	python3 -m venv venv
	. $(VENV); pip install -r requirements.txt

run-back:

insert-index:

run-front: