from __future__ import annotations

def get_first_available_value(dictionary,
                              candidate_keys,
                              default = None):
    """
    Return the first available non-None value from a dictionary.
    """

    for key in candidate_keys:
        if key in dictionary and dictionary[key] is not None:
            return dictionary[key]

    return default
