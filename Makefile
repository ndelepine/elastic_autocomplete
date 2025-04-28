VENV = ./activate_venv

venv: 
	python3 -m venv venv
	. $(VENV); pip install -r requirements.txt

run-back:
	cd back && docker-compose up -d

stop-back:
	cd back && docker-compose stop

insert-index:
	cd back/python && python insert_fake_data.py

run-front:
	cd front && npm run dev