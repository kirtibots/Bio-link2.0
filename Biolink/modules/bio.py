import re
import asyncio
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Biolink import Biolink as app
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, OTHER_LOGS, BOT_USERNAME, SUPPORT_CHAT, UPDATES_CHANNEL
from Biolink.helper.auth import get_auth_users


# ───────────────── MongoDB ─────────────────
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo["BioFilterBot"]
bio_filter = db["bio_filter"]


# ───────────────── Regex ─────────────────
URL_PATTERN = re.compile(r"(https?://|www\.)\S+", re.IGNORECASE)
USERNAME_PATTERN = re.compile(r"@[\w_]+", re.IGNORECASE)


# ───────────────── Filter Status ─────────────────
async def is_enabled(chat_id: int) -> bool:
    data = await bio_filter.find_one({"chat_id": chat_id})
    return bool(data and data.get("enabled", False))


async def set_enabled(chat_id: int, status: bool):
    await bio_filter.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )


# ───────────────── Admin Check ─────────────────
async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in (
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER
        )
    except:
        return False


# ───────────────── Enable / Disable ─────────────────
@app.on_message(filters.command("biolink") & filters.group)
async def bl_cmd(client, message):

    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text(
            "❖ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ υsᴇ ᴛʜɪs ᴄσᴍᴍᴀɴᴅ."
        )

    if len(message.command) < 2:
        return await message.reply_text(
            "**❖ υsᴀɢᴇ :**\n`/biolink on`\n`/biolink off`"
        )

    state = message.command[1].lower()

    if state == "on":
        await set_enabled(message.chat.id, True)
        return await message.reply_text("✅ ❖ ʙɪσ ʟɪɴᴋ ғɪʟᴛᴇʀ **ᴇɴᴀʙʟᴇᴅ**")

    if state == "off":
        await set_enabled(message.chat.id, False)
        return await message.reply_text("❌ ❖ ʙɪσ ʟɪɴᴋ ғɪʟᴛᴇʀ **ᴅɪsᴀʙʟᴇᴅ**")


# ───────────────── Bio Filter ─────────────────
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
        bio = user_info.bio or ""
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

    mention = f"[{user.first_name}](tg://user?id={user.id})"
    username = f"@{user.username}" if user.username else "None"


    # ───── Warning Message ─────
    try:
        warn = await message.reply_text(
            f"⚠️ {mention}\n\n"
            f"❖ **ʏσυʀ ʙɪσ ᴄσɴᴛᴀɪɴs ᴀ ʟɪɴᴋ σʀ υsᴇʀɴᴀᴍᴇ !**\n"
            f"❖ ᴘʟᴇᴀsᴇ ʀᴇᴍσᴠᴇ ɪᴛ ᴛσ sᴇɴᴅ ᴍᴇssᴀɢᴇs ɪɴ ᴛʜɪs ɢʀσυᴘ.",
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close")
                    ],
                    [
                        InlineKeyboardButton("🆘 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
                        InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/{UPDATES_CHANNEL}")
                    ]
                ]
            ),
        )

        await asyncio.sleep(10)
        await warn.delete()

    except:
        pass


    # ───── Log Message ─────
    log_text = f"""
🚨 **ʙɪσ ғɪʟᴛᴇʀ ᴀʟᴇʀᴛ**

❖ **υsᴇʀ :** {mention}
❖ **υsᴇʀɴᴀᴍᴇ :** {username}
❖ **υsᴇʀ ɪᴅ :** `{user.id}`

❖ **ɢʀσυᴘ :** {message.chat.title}
❖ **ᴄʜᴀᴛ ɪᴅ :** `{chat_id}`

❖ **ʙɪσ :**
`{bio}`
"""

    try:
        await client.send_message(
            OTHER_LOGS,
            log_text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "➕ ᴀᴅᴅ ʙᴏᴛ",
                            url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                        )
                    ],
                    [
                        InlineKeyboardButton("🆘 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
                        InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/{UPDATES_CHANNEL}")
                    ]
                ]
            ),
        )
    except:
        pass
