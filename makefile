new_release:
	git checkout master
	git pull origin master
	echo "git tag -a v1.4 -m 'my version 1.4'"
	echo "git push origin v1.4"

deploy:
	git checkout master
	git pull origin master
	git push heroku master

run:
	python manage.py runserver

setup:
	pip install -r requirements.txt

clean_local_branches:
	git branch | grep -v "master" | xargs git branch -D


migrations:
	python manage.py makemigrations bills

migrate:
	python manage.py migrate
