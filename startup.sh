#!/bin/bash
echo "startup script";
if [ ! -f config/settings/config.json ]; then
  cp config/settings/config.template.json config/settings/config.json;
fi
whoami;
su postgres -c "createdb texaslan";
su postgres -c "python manage.py migrate";
gulp;
su postgres -c "python manage.py runserver 0.0.0.0:8000"
