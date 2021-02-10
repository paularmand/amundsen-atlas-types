import os

from atlasclient.client import Atlas


class AtlasClient:
    host = os.environ.get('ATLAS_HOST', 'localhost')
    config = {
        "port": int(os.environ.get('ATLAS_PORT', 21000)),
        "username": os.environ.get('ATLAS_USERNAME', 'admin'),
        "password": os.environ.get('ATLAS_PASSWORD', 'admin'),
        "oidc_token": os.environ.get('ATLAS_BEARER', None),
        "timeout": os.environ.get('ATLAS_REQUEST_TIMEOUT', 10)
    }

    def driver(self):
        print(self.config)
        return Atlas(self.host, **self.config)

driver = AtlasClient().driver()
