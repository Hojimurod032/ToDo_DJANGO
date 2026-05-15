make mig:
	python manage.py makemigrations
	python manage.py migrate
make run:
	python manage.py runserver
