import requests
import json
import MongoDB
import secrets

URL = "https://api.safetyculture.io"  # live site
# URL = "https://sandpit-api.safetyculture.io"  # sand box
HEADER = {'Authorization': 'Bearer {}'.format(secrets.get_token())}  # live site

def sync_with_api():
    pass
