 FROM python:3.6
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /app
 WORKDIR /app
 ADD . /app/
 RUN  pip install -r requirements/local.txt && \
      apt-get update                        && \
      apt-get -y install sudo               && \
      apt-get -y install vim                && \
      curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash - && \
      sudo apt-get install -y nodejs        && \
      npm install --no-optional             && \
      npm install --global gulp-cli         && \
      mv config/settings/config.template.json config/settings/config.json

