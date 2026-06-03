from __future__ import annotations

import os

def get_sirius_base_url(port = None):
    """
    Get the local SIRIUS REST API URL.

    If port is None, the function reads the port used by SIRIUS 6 from
    ~/.sirius/sirius-6.port.
    """

    if port is None:
        port_file = os.path.expanduser("~/.sirius/sirius-6.port")

        if not os.path.isfile(port_file):
            raise FileNotFoundError("Could not find ~/.sirius/sirius-6.port. "
                                    "Keep SIRIUS open, or pass port manually.")

        with open(port_file, "r") as file:
            port = file.read().strip()

    base_url = "http://localhost:" + str(port)

    return base_url
