from __future__ import annotations

import re

def safe_html_name(value):
    """
    Convert molecule names / feature IDs into safe file-name text.
    """

    value = str(value)
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    value = value.strip("_")

    return value
