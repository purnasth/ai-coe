import os
import requests
from config import API_TOKEN_URL, CLIENT_ID


def refresh_access_token():
    """
    Fetches a new accessToken using the refreshToken and sets it in os.environ['VYAGUTA_ACCESS_TOKEN'].
    """
    refresh_token = os.getenv("VYAGUTA_REFRESH_TOKEN")
    if not refresh_token:
        print("Error: VYAGUTA_REFRESH_TOKEN not set in environment.")
        return None
    payload = {"clientId": CLIENT_ID, "refreshToken": refresh_token}
    try:
        response = requests.post(API_TOKEN_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        access_token = data.get("accessToken")
        if access_token:
            os.environ["VYAGUTA_ACCESS_TOKEN"] = access_token
            print("[INFO] Refreshed VYAGUTA_ACCESS_TOKEN.")
            return access_token
        else:
            print("Error: No accessToken in response.")
            return None
    except Exception as e:
        print(f"Error refreshing access token: {e}")
        return None


def app_startup():
    refresh_access_token()
