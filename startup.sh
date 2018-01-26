#!/bin/bash
echo "startup script";
whoami;
su postgres -c "createdb texaslan";
su postgres -c "python manage.py migrate";
gulp;
su postgres -c "python manage.py runserver 0.0.0.0:8000"
