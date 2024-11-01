#Steps to run docker container

1 - docker compose build    or   docker-compose build
2 - docker compose up

#MIGRATIONS

Must follow while migrating ===> Mention app name while migrations at firt else leads to migrations inconsistent issues
Do:
python manage.py makemigrations common

python manage.py migrate common 

#MEDIA
To store images create a media directory gloablly
