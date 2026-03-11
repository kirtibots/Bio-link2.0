import os
from os import getenv

# ------------------------------------------------

API_ID = int(os.environ.get("API_ID", "28795512"))
API_HASH = os.environ.get("API_HASH", "c17e4eb6d994c9892b8a8b6bfea4042a")

# ------------------------------------------------

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@Mafiyamusic_bot")

# -----------------------------------------------

OWNER_ID = int(os.environ.get("OWNER_ID", "8364016757"))
SPECIAL_ID = int(os.environ.get("SPECIAL_ID", "8364016757"))
# ------------------------------------------------

# ------------------------------------------------
LOGGER_ID = int(os.environ.get("LOGGER_ID", ""))

OTHER_LOGS = int(os.environ.get("OTHER_LOGS", ""))

# ------------------------------------------------

MONGO_URL = os.environ.get("MONGO_URL", "")

# ------------------------------------------------
