import os
import sys
from base64 import b64encode

import requests
from dotenv import load_dotenv

load_dotenv()
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

if client_id is None:
    sys.exit("ERROR: CLIENT_ID not found in environment variables")

if client_secret is None:
    sys.exit("ERROR: CLIENT_SECRET not found in environment variables")

basic_auth = f"{client_id}:{client_secret}"
basic_auth_bytes = str.encode(basic_auth)
auth_b64encoded_bytes = b64encode(basic_auth_bytes)

# TODO: may be worth using an OAuth SDK
auth_response = requests.post(
    "https://accounts.spotify.com/api/token",
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_b64encoded_bytes.decode()}",
    },
    data={
        "grant_type": "client_credentials"
    },  #! this auth type is only valid for server to server -> cannot use any APIs for user data
)

if auth_response.status_code != 200:
    sys.exit(f"ERROR: Authentication failed - {auth_response}")

auth_response_body = auth_response.json()

access_token = auth_response_body.get("access_token")

search_query_response = requests.get(
    "https://api.spotify.com/v1/search",
    params={
        "limit": 10,
        "type": "track",
        "q": "King Kunta",
    },
    headers={
        "Authorization": f"Bearer {access_token}",
    },
)

if search_query_response.status_code != 200:
    sys.exit(
        f"ERROR: GET user's top tracks request failed - {search_query_response.json()}"
    )

search_query_response_body = search_query_response.json()

print("search_query_response_body", search_query_response_body)
