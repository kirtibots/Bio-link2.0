from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Biolink import Biolink as app


# ===============================
# ✨ 𝐇ᴇʟᴘ 𝐌ᴇɴᴜ
# ===============================

@app.on_callback_query(filters.regex("^show_help$"))
async def show_help(_, query: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👮 𝐀ᴅᴍɪɴ", callback_data="help_admin"),
                InlineKeyboardButton("⚙️ 𝐆ᴇɴᴇʀᴀʟ", callback_data="help_general")
            ],
            [
                InlineKeyboardButton("👑 𝐎ᴡɴᴇʀ", callback_data="help_owner"),
                InlineKeyboardButton("📊 𝐒ᴛᴀᴛs", callback_data="help_stats")
            ],
            [
                InlineKeyboardButton("⬅️ 𝐁ᴀᴄᴋ", callback_data="back_to_start")
            ]
        ]
    )

    text = """
✨ **𝐔ʟᴛʀᴀ 𝐇ᴇʟᴘ 𝐏ᴀɴᴇʟ**

❖ 𝐒ᴇʟᴇᴄᴛ ᴀ 𝐂ᴏᴍᴍᴀɴᴅ 𝐂ᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ 👇
"""

    await query.message.edit_text(text, reply_markup=keyboard)


# ===============================
# 👮 𝐀ᴅᴍɪɴ 𝐂ᴏᴍᴍᴀɴᴅs
# ===============================

@app.on_callback_query(filters.regex("^help_admin$"))
async def help_admin(_, query: CallbackQuery):

    text = """
👮 **𝐀ᴅᴍɪɴ 𝐂ᴏᴍᴍᴀɴᴅs**

➻ `/auth` → 𝐀ᴅᴅ 𝐁ɪᴏ 𝐔sᴇʀ  
➻ `/rmauth` → 𝐑ᴇᴍᴏᴠᴇ 𝐁ɪᴏ 𝐔sᴇʀ  
➻ `/biolink on` → 𝐄ɴᴀʙʟᴇ 𝐅ɪʟᴛᴇʀ  
➻ `/biolink off` → 𝐃ɪsᴀʙʟᴇ 𝐅ɪʟᴛᴇʀ
"""

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ 𝐁ᴀᴄᴋ", callback_data="show_help")]]
    )

    await query.message.edit_text(text, reply_markup=keyboard)


# ===============================
# ⚙️ 𝐆ᴇɴᴇʀᴀʟ
# ===============================

@app.on_callback_query(filters.regex("^help_general$"))
async def help_general(_, query: CallbackQuery):

    text = """
⚙️ **𝐆ᴇɴᴇʀᴀʟ 𝐂ᴏᴍᴍᴀɴᴅs**

➻ `/start` → 𝐒ᴛᴀʀᴛ 𝐓ʜᴇ 𝐁ᴏᴛ  
➻ `/help` → 𝐎ᴘᴇɴ 𝐇ᴇʟᴘ 𝐌ᴇɴᴜ
"""

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ 𝐁ᴀᴄᴋ", callback_data="show_help")]]
    )

    await query.message.edit_text(text, reply_markup=keyboard)


# ===============================
# 👑 𝐎ᴡɴᴇʀ
# ===============================

@app.on_callback_query(filters.regex("^help_owner$"))
async def help_owner(_, query: CallbackQuery):

    text = """
👑 **𝐎ᴡɴᴇʀ 𝐂ᴏᴍᴍᴀɴᴅs**

➻ `/addsudo` → 𝐀ᴅᴅ 𝐒ᴜᴅᴏ  
➻ `/delsudo` → 𝐑ᴇᴍᴏᴠᴇ 𝐒ᴜᴅᴏ  
➻ `/broadcast` → 𝐁ʀᴏᴀᴅᴄᴀsᴛ 𝐌ᴇssᴀɢᴇ
"""

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ 𝐁ᴀᴄᴋ", callback_data="show_help")]]
    )

    await query.message.edit_text(text, reply_markup=keyboard)


# ===============================
# 📊 𝐒ᴛᴀᴛs
# ===============================

@app.on_callback_query(filters.regex("^help_stats$"))
async def help_stats(_, query: CallbackQuery):

    text = """
📊 **𝐁ᴏᴛ 𝐒ᴛᴀᴛs**

➻ `/stats` → 𝐂ʜᴇᴄᴋ 𝐁ᴏᴛ 𝐒ᴛᴀᴛɪsᴛɪᴄs
"""

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ 𝐁ᴀᴄᴋ", callback_data="show_help")]]
    )

    await query.message.edit_text(text, reply_markup=keyboard)
