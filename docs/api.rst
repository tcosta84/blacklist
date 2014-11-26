===
API
===

Authentication
==============

The Acotel Baclklist APIs use a simple token-based HTTP Authentication scheme.

For client applications to authenticate, the token key should be included in the Authorization HTTP 
header. The key should be prefixed by the string literal "Token", with whitespace separating the 
two strings. For example:::

    Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

Requests without the Authorization header will result in a HTTP 403 Forbidden response:::

    {"detail": "Authentication credentials were not provided."}

Requests with invalid token will also result in a HTTP 403 Forbidden response:::

    {"detail": "Invalid token"}

Generating Tokens
-----------------

To allow a client application to interact with the APIs, admin must create a user/token for the 
this application on the Admin Interface.

Memcached
=========

Memcached is a high-performance, distributed memory object caching system intended for use in 
speeding up dynamic web applications by alleviating database load.

The Acotel Blacklist APIs use Memcached in order to improve performance.

A process runs every 30 minutes checking if the cache exists. If it does not exist, then it is 
recreated:

.. image:: _static/flow_memcached.png

When deleting a customer (using the Delete API or the Admin Interface), only this customer is 
removed from the cache. The same happens when creating a new customer; this new customer is added
immediately to the cache.

Actions
=======

List Customers
--------------

This action allows client applications to view all the customers currently blacklisted:
   
**HTTP Method**::
    
    GET

**URL**::

    http://localhost:8000/customers

**Required headers**::

    Authorization: Token {application_token}

**Response**::

    {
        "count": 3, 
        "next": "http://localhost:8000/customers/?page=2", 
        "previous": null, 
        "results": [
            {
                "id": 18, 
                "url": "http://localhost:8000/customers/5521981520010", 
                "msisdn": 5521981520010, 
                "date_inserted": "2014-11-12T13:02:09.078Z"
            }, 
            {
                "id": 17, 
                "url": "http://localhost:8000/customers/5521981520009", 
                "msisdn": 5521981520009, 
                "date_inserted": "2014-11-12T13:02:03.765Z"
            }
    }

**Expected HTTP Code**::

    200 OK

Example using curl command line tool:::

    curl -X GET http://127.0.0.1:8000/customers/ -H 'Authorization: Token 7455bfd68d00537c319d7e793a8ad4eb266ec9e3' -H 'Accept: application/json; indent=4'

**Pagination**

Client applications can paginate the results using a query parameter "page". For example:::

    http://localhost:8000/customers?page=1

The number of items per page defaults to 10. Client applicatios can override this number using 
"?page_size=x"

Create Customers
----------------

This action allows client applications to add new customers to the blacklist:
   
**HTTP Method**::
    
    POST

**URL**::

    http://localhost:8000/customers

**Required headers**::

    Authorization: Token {application_token}
    Content-type: application/json

**Request**::

        {
            "msisdn": 5521981520011
        }

**Response**::

        {
            "id": 19, 
            "url": "http://localhost:8000/customers/5521981520011", 
            "msisdn": 5521981520011, 
            "date_inserted": "2014-11-12T13:02:09.078Z"
        } 

**Expected HTTP Code**::

    201 CREATED         - customer created successfully
    404 BAD REQUEST     - customer was not created

Example using curl command line tool:::

    curl -X POST http://127.0.0.1:8000/customers/ -d '{"msisdn": 5521981520000}' -H 'Authorization: Token 7455bfd68d00537c319d7e793a8ad4eb266ec9e3' -H 'Content-type: application/json' -H 'Accept: application/json; indent=4'

Retrieve Customer
-----------------

This action allows client applications to view information for a specific customer:

**HTTP Method**::
    
    GET

**URL**::
    
    http://localhost:8000/customers/5521981520010"

**Required headers**::

    Authorization: Token {application_token}

**Response content**::

    {
        "id": 18, 
        "url": "http://localhost:8000/customers/5521981520010", 
        "msisdn": 5521981520010, 
        "date_inserted": "2014-11-12T13:02:09.078Z"
    }

**Expected HTTP Code**::

    200 OK          - customer exists;
    404 NOT FOUND   - customer does not exist.

Example using curl command line tool:::

    curl -X GET http://127.0.0.1:8000/customers/5521981520000/ -H 'Authorization: Token 7455bfd68d00537c319d7e793a8ad4eb266ec9e3' -H 'Accept: application/json; indent=4'

Delete Customer
---------------

This action allows client applications to delete a specific customer:

**HTTP Method**::
    
    DELETE

**URL**::
    
    http://localhost:8000/customers/1/

**Required headers**::

    Authorization: Token {application_token}

**Response content**::

    # empty

**Expected HTTP Code**::

    204 NO CONTENT
    
Example using curl command line tool:::

    curl -X DELETE http://127.0.0.1:8000/customers/5521981520000/ -H 'Authorization: Token 7455bfd68d00537c319d7e793a8ad4eb266ec9e3'

Browsable API
=============

The Acotel Blacklist supports generating human-friendly HTML output for each resource when the 
HTML format is requested. These pages allow for easy browsing of resources.

To see it in action just access the APIs using a browser.
