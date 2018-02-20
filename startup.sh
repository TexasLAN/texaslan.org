#!/bin/bash
echo "startup script";
if [ ! -f config/settings/config.json ]; then
  cp config/settings/config.template.json config/settings/config.json;
fi
whoami;
su postgres -c "createdb texaslan";
su postgres -c "python manage.py migrate";
su postgres -c "python manage.py loaddata user_type_groups.json"
su postgres -c "python manage.py loaddata tags.json"
su postgres -c "python manage.py loaddata test_users.json"
gulp;
su postgres -c "python manage.py runserver 0.0.0.0:8000"
