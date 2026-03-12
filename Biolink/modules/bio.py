# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ ʙɪᴏ ʟɪɴᴋ ғɪʟᴛᴇʀ sʏsᴛᴇᴍ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import re
import asyncio
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from Biolink import Biolink as app
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, OTHER_LOGS, BOT_USERNAME
from Biolink.helper.auth import get_auth_users


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ ᴍᴏɴɢᴏᴅʙ sᴇᴛᴜᴘ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo["BioFilterBot"]

bio_filter = db["bio_filter"]
warn_db = db["bio_warns"]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ ʀᴇɢᴇx ᴘᴀᴛᴛᴇʀɴ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

URL_PATTERN = re.compile(r"(https?://|www\.)\S+", re.IGNORECASE)
USERNAME_PATTERN = re.compile(r"@[\w_]+", re.IGNORECASE)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ ғɪʟᴛᴇʀ sᴛᴀᴛᴜs
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def is_enabled(chat_id: int) -> bool:
    data = await bio_filter.find_one({"chat_id": chat_id})
    return data.get("enabled", False) if data else False


async def set_enabled(chat_id: int, status: bool):
    await bio_filter.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ ᴡᴀʀɴɪɴɢ sʏsᴛᴇᴍ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def get_warn(chat_id, user_id):
    data = await warn_db.find_one({"chat_id": chat_id, "user_id": user_id})
    return data["warn"] if data else 0


async def add_warn(chat_id, user_id):
    warn = await get_warn(chat_id, user_id) + 1
    await warn_db.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"warn": warn}},
        upsert=True
    )
    return warn


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ ᴀᴅᴍɪɴ ᴄʜᴇᴄᴋ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER
        ]
    except:
        return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ /ʙɪᴏʟɪɴᴋ ᴄᴏᴍᴍᴀɴᴅ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("biolink") & filters.group)
async def bio_command(client, message):

    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ **Only Admins Can Use This Command**")

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage :**\n\n`/biolink on`\n`/biolink off`"
        )

    state = message.command[1].lower()

    if state == "on":
        await set_enabled(message.chat.id, True)
        await message.reply_text("✅ **ʙɪᴏ ʟɪɴᴋ ғɪʟᴛᴇʀ ᴇɴᴀʙʟᴇᴅ**")

    elif state == "off":
        await set_enabled(message.chat.id, False)
        await message.reply_text("❌ **ʙɪᴏ ʟɪɴᴋ ғɪʟᴛᴇʀ ᴅɪsᴀʙʟᴇᴅ**")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ ʙɪᴏ ғɪʟᴛᴇʀ ᴍᴀɪɴ sʏsᴛᴇᴍ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.group & filters.text)
async def bio_filter_handler(client, message):

    chat_id = message.chat.id
    user = message.from_user

    if not user:
        return

    if not await is_enabled(chat_id):
        return

    if await is_admin(client, chat_id, user.id):
        return

    auth_data = await get_auth_users(chat_id)
    if user.id in auth_data.get("auth_users", []):
        return

    try:
        user_info = await client.get_chat(user.id)
        bio = getattr(user_info, "bio", "") or ""
    except:
        bio = ""

    if not bio:
        return

    if not (URL_PATTERN.search(bio) or USERNAME_PATTERN.search(bio)):
        return

    try:
        await message.delete()
    except:
        pass


    warn_count = await add_warn(chat_id, user.id)

    mention = f"[{user.first_name}](tg://user?id={user.id})"
    username = f"@{user.username}" if user.username else "None"


    # ⚠️ Warning Message
    try:
        warn_msg = await message.reply_text(
            f"""
⚠️ {mention}

**ʙɪᴏ ᴍᴇ ʟɪɴᴋ / ᴜsᴇʀɴᴀᴍᴇ ᴀʟʟᴏᴡᴇᴅ ɴᴀʜɪ ʜᴀɪ**

🚫 **ᴡᴀʀɴɪɴɢ : {warn_count} / 3**
""",
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")]]
            ),
        )

        await asyncio.sleep(30)
        await warn_msg.delete()

    except:
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ ʟᴏɢ sʏsᴛᴇᴍ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    log_text = f"""
🚨 **ʙɪᴏ ғɪʟᴛᴇʀ ᴀʟᴇʀᴛ**

👤 **ᴜsᴇʀ :** {mention}
🔗 **ᴜsᴇʀɴᴀᴍᴇ :** {username}
🆔 **ᴜsᴇʀ ɪᴅ :** `{user.id}`

👥 **ɢʀᴏᴜᴘ ʟɪɴᴋ :** {message.chat.link}
💬 **ᴄʜᴀᴛ ɪᴅ :** `{chat_id}`

📄 **bio :**
`{bio}`
"""

    try:
        log_msg = await client.send_message(
            OTHER_LOGS,
            log_text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    "➕ ᴀᴅᴅ ʙᴏᴛ",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                )]]
            ),
        )

        await asyncio.sleep(30)
        await log_msg.delete()

    except:
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ ᴡᴀʀɴ ʟɪsᴛ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("warnlist") & filters.group)
async def warn_list(client, message):

    if not await is_admin(client, message.chat.id, message.from_user.id):
        return

    data = warn_db.find({"chat_id": message.chat.id})

    text = "⚠️ **ʙɪᴏ ғɪʟᴛᴇʀ ᴡᴀʀɴ ʟɪsᴛ**\n\n"
    count = 0

    async for user in data:
        count += 3
        text += f"👤 `{user['user_id']}` ➜ {user['warn']} warns\n"

    if count == 3:
        text += "No warnings yet."

    await message.reply_text(text)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✦ ᴄʟᴏsᴇ ʙᴜᴛᴛᴏɴ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("close"))
async def close_button(_, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        pass
