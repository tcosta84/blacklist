Development
===========

To start developing on Acotel Blacklist, first clone the repo:::

    git clone ssh://git@stash.acotelbrasil.com.br:7999/blist/blacklist.git

Setup
#####

To setup the application, clone the repository, and then:::

    cd {project_path}
    virtualenv env
    source env/bin/activate
    pip install -r requirements.pip

Then create a .env text file next to the manage.py file in the form:::

    DEBUG=True
    SECRET_KEY=ypfj76g@yp#f7b$u&-1w1+&715$mqu^z4u^o6g1^q2uhv3vblt
    DATABASE_URL=postgres://{{db_user}}:{{db_pass}}@localhost:5432/blacklist
    MEMCACHED_LOCATION=localhost:11211
    STATIC_ROOT=/static/
    MEDIA_ROOT=/media/
    LOGGING_ROOT=/tmp/

It's recommended you generate your own unique SECRET_KEY.
You can do this using the Python interactive interpreter. Just run the command .manage.py shell 
and insert the code below, then copy and paste the generated key on your .env file:::

    from django.utils.crypto import get_random_string
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    get_random_string(50, chars)

Finally you can launch the development server and start coding:

    ./manage.py runserver

Testing
#######

To run the tests, clone the repository, setup the application and then:::

    ./manage.py test

Best practices
##############

Code changes should broadly follow the PEP 8 style conventions, and we recommend you setup your 
editor to automatically indicated non-conforming styles.

Deploy
######

ToDo
