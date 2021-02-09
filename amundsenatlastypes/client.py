import os

from atlasclient.client import Atlas


class AtlasClient:
    config = {
        host: os.environ.get('ATLAS_HOST', 'localhost'),
        port: os.environ.get('ATLAS_PORT', 21000),
        user: os.environ.get('ATLAS_USERNAME', 'admin'),
        password: os.environ.get('ATLAS_PASSWORD', 'admin'),
        oidc_token: os.environ.get('ATLAS_BEARER', None),
        timeout: os.environ.get('ATLAS_REQUEST_TIMEOUT', 10)
    }

    def driver(self):
        return Atlas(**config)

driver = AtlasClient().driver()
