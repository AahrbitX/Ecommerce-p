#Steps to run docker container

1 - docker compose build    or   docker-compose build
2 - docker compose up

#MIGRATIONS

Must follow while migrating ===> Mention app name while make migrations at first else leads to migrations inconsistent issues
Do:
python manage.py makemigrations common

python manage.py migrate common 

following "python manage.py migrate"  to migrate admin details

#MEDIA
To store images create a media directory gloablly
