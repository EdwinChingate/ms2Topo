from __future__ import annotations

import requests

def sirius_get_json(base_url,
                    endpoint):
    """
    Query one SIRIUS REST endpoint and return JSON.
    """

    url = base_url.rstrip("/") + endpoint

    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError("SIRIUS request failed.\n"
                           f"URL: {url}\n"
                           f"Status: {response.status_code}\n"
                           f"Text: {response.text[:1000]}")

    return response.json()
