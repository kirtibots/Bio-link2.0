# ✦ 𝐀𝐚𝐬𝐡𝐢𝐤 𝐓ᴇᴀᴍ 𝐀𝐮𝐭𝐡 𝐒𝐲𝐬𝐭𝐞𝐦

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from Biolink import Biolink as app
from Biolink.helper.auth import add_auth, remove_auth, get_auth_users
from Biolink.helper.admin import is_admins


# ───────────────────────
# ✦ 𝐅𝐎𝐑𝐌𝐀𝐓 𝐔𝐒𝐄𝐑
# ───────────────────────

def format_user(user):
    username = f"@{user.username}" if user.username else "No Username"
    mention = user.mention(style="markdown")

    return (
        f"❍ **𝐍𝐚𝐦𝐞 :** {mention}\n"
        f"❍ **𝐔𝐬𝐞𝐫 𝐈𝐃 :** `{user.id}`\n"
        f"❍ **𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞 :** `{username}`"
    )


# ───────────────────────
# ✦ 𝐆𝐄𝐓 𝐔𝐒𝐄𝐑
# ───────────────────────

async def get_target_user(message: Message):

    if message.reply_to_message:
        return message.reply_to_message.from_user

    if len(message.command) > 1:
        user_input = message.command[1]

        try:
            user = await app.get_users(user_input)
            return user
        except:
            return None

    return None


# ───────────────────────
# ✦ 𝐀𝐔𝐓𝐇 𝐔𝐒𝐄𝐑
# ───────────────────────

@app.on_message(
    filters.command("auth", prefixes=["/", "!", "%", ",", ".", "@", "#"]) & filters.group
)
async def add_auth_command(client, message: Message):

    if not await is_admins(message.chat.id, message.from_user.id):
        return await message.reply(
            "❌ **𝐎𝐧𝐥𝐲 𝐆𝐫𝐨𝐮𝐩 𝐎𝐰𝐧𝐞𝐫 𝐎𝐫 𝐀𝐝𝐦𝐢𝐧𝐬 𝐂𝐚𝐧 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 !**"
        )

    user = await get_target_user(message)

    if not user:
        return await message.reply(
            "⚠️ **𝐑𝐞𝐩𝐥𝐲 𝐓𝐨 𝐀 𝐔𝐬𝐞𝐫 𝐎𝐫 𝐆𝐢𝐯𝐞 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞 / 𝐔𝐬𝐞𝐫 𝐈𝐃 !**"
        )

    await add_auth(message.chat.id, user.id)

    await message.reply(
        f"✅ **𝐔𝐬𝐞𝐫 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 !**\n\n{format_user(user)}"
    )


# ───────────────────────
# ✦ 𝐑𝐄𝐌𝐎𝐕𝐄 𝐀𝐔𝐓𝐇
# ───────────────────────

@app.on_message(
    filters.command("rmauth", prefixes=["/", "!", "%", ",", ".", "@", "#"]) & filters.group
)
async def remove_auth_command(client, message: Message):

    if not await is_admins(message.chat.id, message.from_user.id):
        return await message.reply(
            "❌ **𝐎𝐧𝐥𝐲 𝐆𝐫𝐨𝐮𝐩 𝐎𝐰𝐧𝐞𝐫 𝐎𝐫 𝐀𝐝𝐦𝐢𝐧𝐬 𝐂𝐚𝐧 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 !**"
        )

    user = await get_target_user(message)

    if not user:
        return await message.reply(
            "⚠️ **𝐑𝐞𝐩𝐥𝐲 𝐓𝐨 𝐀 𝐔𝐬𝐞𝐫 𝐎𝐫 𝐆𝐢𝐯𝐞 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞 / 𝐔𝐬𝐞𝐫 𝐈𝐃 !**"
        )

    await remove_auth(message.chat.id, user.id)

    await message.reply(
        f"❌ **𝐔𝐬𝐞𝐫 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 !**\n\n{format_user(user)}"
    )


# ───────────────────────
# ✦ 𝐀𝐔𝐓𝐇 𝐋𝐈𝐒𝐓
# ───────────────────────

@app.on_message(
    filters.command("authlist", prefixes=["/", "!", "%", ",", ".", "@", "#"]) & filters.group
)
async def authlist_handler(client, message: Message):

    if not await is_admins(message.chat.id, message.from_user.id):
        return await message.reply(
            "❌ **𝐎𝐧𝐥𝐲 𝐀𝐝𝐦𝐢𝐧𝐬 𝐂𝐚𝐧 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 !**"
        )

    chat_id = message.chat.id
    data = await get_auth_users(chat_id)

    users = data.get("auth_users", [])

    if not users:
        return await message.reply(
            "⚠️ **𝐍𝐨 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐔𝐬𝐞𝐫𝐬 𝐅𝐨𝐮𝐧𝐝 !**"
        )

    text = "🔐 **𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐔𝐬𝐞𝐫𝐬 𝐈𝐧 𝐓𝐡𝐢𝐬 𝐆𝐫𝐨𝐮𝐩**\n\n"

    for i, user_id in enumerate(users, start=1):

        try:
            user = await app.get_users(user_id)
            name = user.mention(style="markdown")
        except:
            name = f"`{user_id}`"

        text += f"➤ {i}. {name}\n"

    await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✘ 𝐂𝐥𝐨𝐬𝐞", callback_data="close_auth")]]
        )
    )


# ───────────────────────
# ✦ 𝐂𝐋𝐎𝐒𝐄 𝐁𝐔𝐓𝐓𝐎𝐍
# ───────────────────────

@app.on_callback_query(filters.regex("close_auth"))
async def close_button(client, query: CallbackQuery):

    try:
        await query.message.delete()
    except:
        pass
