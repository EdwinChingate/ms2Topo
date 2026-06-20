from __future__ import annotations

import re

def sanitize_attribute_name(name):
    """
    Make a column name safer for NetworkX export formats such as GraphML/GEXF.
    """

    name = str(name)
    name = name.strip()
    name = re.sub(r"\s*\|\s*", "_", name)
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^A-Za-z0-9_]+", "_", name)
    name = re.sub(r"_+", "_", name)
    name = name.strip("_")

    return name
