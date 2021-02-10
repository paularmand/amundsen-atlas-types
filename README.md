# Amundsen Atlas Types
[![PyPI version](https://badge.fury.io/py/amundsenatlastypes.svg)](https://badge.fury.io/py/amundsenatlastypes)
[![Build Status](https://api.travis-ci.org/dwarszawski/amundsen-atlas-types.svg?branch=master)](https://travis-ci.org/dwarszawski/amundsen-atlas-types)
[![License](http://img.shields.io/:license-Apache%202-blue.svg)](LICENSE)

Kickstart your Apache Atlas to support Amundsen using the prebuilt functions and required entity definitions.  

## Installation:
The package is available on PyPi, which you can install using below. 

```bash
    pip install amundsenatlastypes
```

## Usage:

#### Connecting to Apache Atlas:
`amundsenatlastypes` uses environment variables to connect to Apache Atlas. 

Following are the environment variables need to be set in order to connect to 
Apache Atlas. 

```bash
- ATLAS_HOST                [default = localhost]
- ATLAS_PORT                [default = 21000]
- ATLAS_USERNAME            [default = admin]
- ATLAS_PASSWORD            [default = admin]
```

For connecting to Purview, see below.

#### Kickstart Apache Atlas
A single python function is available that you can use to apply all required entity definitions. 
You can run this function as many times as you want, and it will not break any existing functionality, that means
that it can also be implemented in your pipelines. 

```python
from amundsenatlastypes import Initializer
    
init = Initializer()
init.create_required_entities()
```

There also is a functionality to initiate your existing data to work accordingly with Amundsen. 
To create required relations you need to set `fix_existing_data=True` while calling the `create_required_entities()`.

```python
from amundsenatlastypes import Initializer
    
init = Initializer()
init.create_required_entities(fix_existing_data=True)
```


#### Functionality:
`amundsenatlastypes` provides a number of functions that can be used separately to 
implement/apply entity definitions of Apache Atlas, which are available [here](/amundsenatlastypes/__init__.py).


You can also simply access the individual entity definitions in JSON format by importing them 
from [here](amundsenatlastypes/types.py).  

#### Purview:
`amundsenatlastypes` will set all new types on Purview, and also handle the new relationships. Some entity definitions
such as `sap_s4hana_table` are build-in types provided by Azure in Purview, and Azure Purview API complains when we ask to
update them (`amundsenatlastypes` tries to make all *_table entities a subtype of Table). The same happens for the column
definitions of the build-in table types. Watch the terminal output for these Errors, and you can see what was changed and what not. 


##### Connecting to Azure Purview:
`amundsenatlastypes` uses environment variables to connect to Purview. 

Following are the environment variables need to be set in order to connect to Purview, but the example does this from python.
You then need to use the msal library to get an oidc token to give to `amundsenatlastypes` like so:

```python
import msal
import logging
import os

os.environ['TENANT'] = "your tenant id"
os.environ['ATLAS_HOST'] = "https://mypurview.catalog.purview.azure.com"
os.environ['ATLAS_PORT'] = "443"
os.environ['ATLAS_USERNAME'] = "this is the clientid of the enterprise app"
os.environ['ATLAS_PASSWORD'] = "this is the value of the secret in the configuration of the enterprise app"  

config = {
  "authority": "https://login.microsoftonline.com/" + os.environ['TENANT'],
  "client_id": os.environ['ATLAS_USERNAME'],
  "scope": [ "https://purview.azure.net/.default" ],
  "secret": os.environ['ATLAS_PASSWORD'],
  "endpoint": os.environ['ATLAS_HOST'],
}

# Create a preferably long-lived app instance that maintains a token cache.
app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"],
    # token_cache=...  # Default cache is in memory only.
                       # You can learn how to use SerializableTokenCache from
                       # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )

# The pattern to acquire a token looks like this.
result = None

# First, the code looks up a token from the cache.
# Because we're looking for a token for the current app, not for a user,
# use None for the account parameter.
result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])

if "access_token" in result:
    # Call a protected API with the access token.
    print(result["token_type"])
    
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You might need this when reporting a bug.

# store the oidc token in an environment variable
os.environ['ATLAS_BEARER'] = result["access_token"]

# the rest is the same as for Atlas
from amundsenatlastypes import Initializer
    
init = Initializer()
init.create_required_entities()
```
