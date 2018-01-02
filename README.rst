texaslan.org
=======

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/texaslan/texaslan.org/master/LICENSE
    :alt: MIT Licensed

The main online hub for Texas LAN, built with Django. This project is heavily based on this project here_

.. _here: https://github.com/txcsmad/txcsmad.com

* User system
* Event system with QR code check-in
* URL shortener
* Admin panel
* Information about LAN

Development
-----

Local Deployment
^^^^^^^^^^^^^^^^

Get all the dependencies we'll need to run Django.
::
    brew install python3
    git clone git@github.com:texaslan/texaslan.org.git
    pip3 install -r requirements/local.txt

Install Postgres app(http://postgresapp.com/) and start Postgres.
::
    # Create the Postgres DB
    createdb texaslan
    # Populate the DB with test data
    python3 manage.py migrate

We use Gulp_ for our build system. It automates the process of compiling styles and minifying static assets. To install it\:
::
    brew install npm
    npm install
    npm install --global gulp-cli

.. _Gulp: http://gulpjs.com

In ``config/settings``, lename ``config.template.json`` to ``config.json``. The default values should be fine for local development.

Several run configurations are available. Check ``gulpfile.js`` for more details.
::
    # Runs all build steps
    gulp
    # Runs the server
    python3 manage.py runserver

Use ``gulp watch`` to automatically recompile any assets you modify in the background while you work.

Importing test data and users
^^^^^^^^^^^^^^^^^^^^^

Each app includes fixtures_. Load them with
::
    python manage.py loaddata <fixture-name>

Required fixtures for the website to be properly running are the Event Tag fixtures, and the User Type Groups fixtures.

.. _fixtures: https://docs.djangoproject.com/en/1.10/howto/initial-data/

All included test users have the password ``password``.

Running Tests
^^^^^^^^^^^^^
Just run
::
    py.test

Checking Coverage
^^^^^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report
::
    coverage run manage.py test
    coverage html
    open htmlcov/index.html


Manually manipulating data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. In the local environment, check your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

To mark an existing account as superuser and staff
::
    psql texaslan
    texaslan# UPDATE users_user SET is_superuser = true AND is_staff = true WHERE id = 1;

Server Deployment
----------

First time
^^^^^^^^^^
Ensure that Python 3.5 and Postgres are installed, then run the below.
::
    git clone git@github.com:texaslan/texaslan.org.git
    pip3 install -r requirements/production.txt
    npm install
    npm install --global gulp-cli
    createdb texaslan
    python3 manage.py migrate

Install a `Django stack`_ on a DigitalOcean Droplet. You will need more than the base droplet as 512Mb of RAM is too little to install everything.

.. _Django stack: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

Get SSL certificates from `Let's Encrypt`_, and configure Nginx to serve them. You can follow this `tutorial`_ on how to implement this on this Django stack.

.. _tutorial: https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04

.. _Let's Encrypt: https://letsencrypt.org/

Rename ``config.template.json`` to ``config.json`` in ``config/settings``. The Django key should be a unique 50 character key. You can generate a new key here: http://www.miniwebtool.com/django-secret-key-generator/. Make sure that you generate or retrieve the other keys as well.

Updates
^^^^^^^
The LAN server is configured with an ``updatelan`` command, which is an alias for the below.
::
    # Update and use master ( not pull, to enforce using whatever is on master )
    git fetch
    git reset --hard origin/master

    # update pip & python packages
    pip3 install --upgrade pip
    pip3 install -r requirements/production.txt

    # update nodejs packages
    npm install

    # migrate database changes
    python3 manage.py migrate

    # Update sass and js files
    gulp

    # Gather all static files and update them
    python3 manage.py collectstatic --noinput

    # Restart server with new code::
    sudo systemctl restart gunicorn && sudo systemctl restart nginx
