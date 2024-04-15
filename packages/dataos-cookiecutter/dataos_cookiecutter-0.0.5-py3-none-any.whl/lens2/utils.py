import os
import requests

from lens2.constants import LENS2_BASE_URL, LENS2_NAME, LENS2_META_PATH, DATAOS_USER_APIKEY


def get_env_or_throw(env_name):
    """Get the value of an environment variable or raise an error."""
    value = os.getenv(env_name)
    if value is None:
        raise ValueError(f"The environment variable '{env_name}' is not set.")
    return value


def make_api_call_with_headers(api_url, headers):
    """Make an API call with headers."""
    response = requests.get(api_url, headers=headers)
    return response.json()


def get_lens_meta():
    lens2_base_url = get_env_or_throw(LENS2_BASE_URL)
    lens2_name = get_env_or_throw(LENS2_NAME)
    lens2_meta_path = get_env_or_throw(LENS2_META_PATH)
    apikey = get_env_or_throw(DATAOS_USER_APIKEY)

    url = f"{lens2_base_url}/{lens2_name}{lens2_meta_path}?showPrivate=true"
    headers = {"Authorization": apikey}
    return make_api_call_with_headers(url, headers=headers)