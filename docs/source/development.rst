Development
===========

To start developing on Acotel Blacklist, first clone the repo:::

    git clone ssh://git@stash.acotelbrasil.com.br:7999/blist/blacklist.git

Changes should broadly follow the PEP 8 style conventions, and we recommend you setup your 
editor to automatically indicated non-conforming styles.

Setup
#####

To setup the application, clone the repository, and then:::

    virtualenv env
    source env/bin/activate
    pip install -r requirements.pip

Testing
#######

To run the tests, clone the repository, setup the application and then:::

    ./manage.py test

Deploy
######

ToDo
