=========
Tutorials
=========

Generating tokens
=================

To allow your application to interact with the available APIs, a user/token must be created on the
Admin Interface.

Clearing cache
==============

You can clear cache manually by calling the following command:::

    ./manage.py delete_memcached

This is usefull especially if you are redeploying your application and want a fresh install.
