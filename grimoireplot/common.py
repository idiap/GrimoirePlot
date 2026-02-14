# SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
# SPDX-License-Identifier: MIT

"""
Common module for grimoireplot client and server
"""

import os
from dotenv import load_dotenv
from loguru import logger


load_dotenv()


def get_grimoire_secret() -> str:
    if (grimoire_secret := os.environ.get("GRIMOIRE_SECRET")) is None:
        logger.warning("GRIMOIRE_SECRET not set; using default secret")
        grimoire_secret = "IDidntSetASecret"

    return grimoire_secret


def get_grimoire_server() -> str:
    if (grimoire_server := os.environ.get("GRIMOIRE_SERVER")) is None:
        grimoire_server = "http://localhost:8080"
        logger.warning(
            f"GRIMOIRE_SERVER not set; using default server {grimoire_server}"
        )

    return grimoire_server
