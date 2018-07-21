#!/bin/bash
echo "startup script";
if [ ! -f config/settings/config.json ]; then
  cp config/settings/config.template.json config/settings/config.json;
fi
whoami;
python manage.py check;
# wait for database to start up :(
sleep 7;
python manage.py migrate;
python manage.py loaddata user_type_groups.json
python manage.py loaddata tags.json
python manage.py loaddata test_users.json
python manage.py runserver 0.0.0.0:8000;
