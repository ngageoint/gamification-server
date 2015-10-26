#!/bin/bash

WORKDIR="/server"

cd $WORKDIR
pip install -r requirements.txt
python manage.py syncdb --noinput
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
