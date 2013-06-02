Redeer
======

Self-hosted, django-based backend for use with Reeder.


Installation
------------

::
    git clone git://github.com/davidszotten/redeer.git
    cd redeer
    heroku create
    git push heroku master
    SECRET_KEY=`openssl rand -base64 36`
    DOMAIN_NAME=`heroku apps:info -s|grep domain_name|cut -d "=" -f 2`
    heroku config:set SECRET_KEY=$SECRET_KEY DOMAIN_NAME=$DOMAIN_NAME

    heroku run ./manage.py syncdb --noinput
    heroku run ./manage.py migrate
    heroku run ./manage.py collectstatic --noinput

    heroku addons:add scheduler
    heroku addons:open scheduler

Add an hourly task that runs ``./manage.py sync_all``


Inspired by `Stringer <https://github.com/swanson/stringer>`_

Why not use Stringer
--------------------

It didn't support groups, which I need (well, want). Tried to contribute a
patch, but having never really used ruby I gave up and built my own in python.


License
-------

MIT. See LICENSE for details
