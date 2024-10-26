FROM python:3

ENV PYTHONUNBUFFERED=1
  
ARG PROJECT=group
ARG PROJECT_DIR=/var/www/${PROJECT}
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY . .
 
   
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]

EXPOSE 8000
