Development
===========

If you are interested in colaborating with this project, please make sure you read the next steps:

Dependencies
############

These are the mains dependencies. Make sure you have them installed before continuing:::

* Python 2.7.8
* PostgreSQL 9.3.5
* Memcached 1.4.20
* RabbitMQ 3.4.1
* Virtualenv

Repository
##########

Now clone the repository:::
    
    git clone ssh://git@stash.acotelbrasil.com.br:7999/blist/blacklist.git

Setup
#####

Create you virtual environment on your preferred location:::

    virtualenv ~/Virtualenvs/blacklist

Activate this virtualenv:::

    source ~/Virtualenvs/blacklist/bin/activate

Install the python requirements:::

    pip install -r requirements.pip

Create the database:::

    createdb -T template0 -E utf-8 blacklist

Create a .env text file next to the manage.py file in the form:::

    DEBUG=True
    SECRET_KEY=ypfj76g@yp#f7b$u&-1w1+&715$mqu^z4u^o6g1^q2uhv3vblt
    DATABASE_URL=postgres://{{db_user}}:{{db_pass}}@localhost:5432/blacklist
    MEMCACHED_LOCATION=localhost:11211
    RABBITMQ_URL=amqp://guest@localhost//
    STATIC_ROOT=/static/
    MEDIA_ROOT=/media/
    LOGGING_ROOT=/tmp/

It's recommended you generate your own unique SECRET_KEY.
You can do this using the Python interactive interpreter. Just run the command .manage.py shell 
and insert the code below, then copy and paste the generated key on your .env file:::

    from django.utils.crypto import get_random_string
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    get_random_string(50, chars)

Create the database tables:::

    ./manage.py migrate

Launch the development server:::

    ./manage.py runserver

Open a new terminal window/tab and launch the Celery worker so that the cron tasks are executed:::
    
    celery worker -B -A blacklist --autoreload --loglevel debug

Open a new terminal window/tab and launch Flower server so that you can monitor the Celery tasks:::
    
    flower

Finally you can check if everything is running:

    http://localhost:8000/customers
    http://localhost:5000

Testing
#######

You are required to write unit tests for every change you make.
Also make sure you run the test suite before commiting your changes to the repository:::

    ./manage.py test

Coverage
--------

Code coverage describes how much source code has been tested. It shows which parts of your code 
are being exercised by tests and which are not.

To run your tests and also collect coverage data of the executed files, run the following from 
your project folder containing manage.py:::

    coverage run --source='.' manage.py test core

Now you can see a report of this data by typing following command:::
    
    coverage report

You should aim a 100% coverage for every file you create/change, as much as possible.

Best practices
##############

Code Style
----------

Code changes should broadly follow the PEP 8 style conventions, and we recommend you setup your 
editor to automatically indicate non-conforming styles.

Database changes
----------------

Never make changes directly to the database. If you need to create another table or change a
field's table or create a procedure etc, make a migration file and run ./manage.py migrate

Deploy
######

ToDo
