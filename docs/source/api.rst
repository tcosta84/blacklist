===
API
===

Authentication
==============

Every Acotel Baclklist API uses a simple token-based HTTP Authentication scheme.

For applications to authenticate, the token key should be included in the Authorization HTTP 
header. The key should be prefixed by the string literal "Token", with whitespace separating the 
two strings. For example:::

    Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

Requests without the Authorization header will result in a HTTP 403 Forbidden response:::

    {"detail": "Authentication credentials were not provided."}

Requests with invalid token will also result in a HTTP 403 Forbidden response:::

    {"detail": "Invalid token"}

Generating Tokens
-----------------

To allow your application to interact with the available APIs, a user/token must be created on the
Admin Interface.

Memcached
=========

Memcached is a high-performance, distributed memory object caching system intended for use in 
speeding up dynamic web applications by alleviating database load.

All the APIs use Memcached in order to improve performance.

Every request check if cache key "blacklist" exists. If so, the results from the cache are used, 
otherwise results are retrieved from the database and set on the cache for the next request.

When deleting a customer (by Delete API or Admin Interface), this key is deleted and recreated in
the next request.

Available APIs
==============

List Customers API
------------------

The Acotel Blacklist List API allows client applications to view all the customers currently 
blacklisted (status = ACTIVE):
   
**Method**::
    
    GET

**URL**::

    http://localhost:8000/customers

**Response**::

    {
        "count": 3, 
        "next": null, 
        "previous": null, 
        "results": [
            {
                "id": 2, 
                "url": "http://localhost:8000/customers/2/", 
                "msisdn": 21981211250, 
                "date_inserted": "2014-11-10T19:32:27.342Z"
            }, 
            {
                "id": 1, 
                "url": "http://localhost:8000/customers/1/", 
                "msisdn": 21981527318, 
                "date_inserted": "2014-11-10T19:29:12.664Z"
            }, 
            {
                "id": 3, 
                "url": "http://localhost:8000/customers/3/", 
                "msisdn": 21981279218, 
                "date_inserted": "2014-11-11T14:28:00.635Z"
            }
        ]
    }

The curl command line tool may be useful for testing token authenticated APIs. For example:::

    curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

**Pagination**

Client applications can paginate the results using a query parameter "page". For example:::

    http://localhost:8000/customers?page=1

The number of items per page defaults to 10. Client applicatios can override this number using 
"?page_size=x"

**Filtering**

Client applications can also restrict the items that are returned. A common scenario is checking 
if a specific customer is blacklisted. For example:::

    http://localhost:8000/customers?msisdn=21981527318

If "count" is greater than zero than the searched customer is blacklisted.

Retrieve Customer API
---------------------

The Acotel Blacklist Detail API allows client applications to view information for a specific 
customer:

**Method**::
    
    GET

**URL**::
    
    http://localhost:8000/customers/1/

**Response content**::

    [
        {
            "id": 1, 
            "url": "http://localhost:8000/customers/1/", 
            "msisdn": 21981527318, 
            "date_inserted": "2014-11-10T19:29:12.664Z"
        }
    ]

Delete Customer API
-------------------

The Acotel Blacklist Delete API allows client applications to delete (status = DELETED) a 
specific customer:

**Method**::
    
    DELETE

**URL**::
    
    http://localhost:8000/customers/1/

**Response content**::

    # empty

Browsable API
=============

API may stand for Application Programming Interface, but humans have to be able to read the APIs,
too; someone has to do the programming. The Acotel Blacklist supports generating human-friendly
HTML output for each resource when the HTML format is requested. These pages allow for easy
browsing of resources.
