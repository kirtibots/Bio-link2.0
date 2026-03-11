#  ─────────────────────────────────────
#        BioLink Bot Configuration
#  ─────────────────────────────────────

import os

# ---------------- BOT INFO ----------------
API_ID = int(os.getenv("API_ID", "21692000"))
API_HASH = os.getenv("API_HASH", "1e37856155373adf855c061c49847ced")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

BOT_USERNAME = os.getenv("BOT_USERNAME", "YourBotUsername")

# ---------------- DATABASE ----------------
MONGO_URL = os.getenv("MONGO_URL", "")

# ---------------- LOGS ----------------
LOG_GROUP = int(os.getenv("LOG_GROUP", "-1003670001038"))
OTHER_LOGS = int(os.getenv("OTHER_LOGS", "-1003670001038"))

# ---------------- CHANNELS ----------------
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/Kirti_update")
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "https://t.me/kirti_supprot_group")

# ---------------- OWNER ----------------
OWNER_ID = int(os.getenv("OWNER_ID", "5857831018"))

# ---------------- BOT SETTINGS ----------------
START_IMG = os.getenv(
    "START_IMG",
    "https://files.catbox.moe/28m00r.jpg"
)

# ---------------- WARN SETTINGS ----------------
MAX_WARNINGS = int(os.getenv("MAX_WARNINGS", "3"))

# ---------------- HEROKU ----------------
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", None)
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", None)

# ---------------- BOT VERSION ----------------
BOT_VERSION = "2.0"
