from __future__ import annotations

def normalize_sirius_list(response_object):
    """
    Normalize SIRIUS API responses that may be either a list, a page object,
    or a dictionary containing list-like values.
    """

    if isinstance(response_object, list):
        return response_object

    if isinstance(response_object, dict):

        for key in ["content",
                    "items",
                    "features",
                    "alignedFeatures",
                    "formulaCandidates",
                    "formulas"]:
            if key in response_object and isinstance(response_object[key], list):
                return response_object[key]

        embedded = response_object.get("_embedded", None)

        if isinstance(embedded, dict):
            for value in embedded.values():
                if isinstance(value, list):
                    return value

    return []
