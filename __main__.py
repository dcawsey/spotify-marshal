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

auth_response = requests.post(
    "https://accounts.spotify.com/api/token",
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_b64encoded_bytes.decode()}",
    },
    data={"grant_type": "client_credentials"},
)

if auth_response.status_code != 200:
    sys.exit(f"Authentication failed: {auth_response.json()}")

response_body = auth_response.json()

access_token = response_body.get("access_token")
