from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.enums import ChatType

from config import OWNER_ID, BOT_USERNAME
from Biolink import Biolink as app
from Biolink.helper.database import add_user, add_chat

START_IMG = "https://files.catbox.moe/gdjna3.jpg"

def get_start_caption(user):
    return f"""
text = """
✨ ʜᴇʏ {user.mention} !

🤖 ɪ ᴀᴍ ᴀɴ ᴀᴜᴛᴏ ʟɪɴᴋ ʀᴇᴍᴏᴠᴇʀ ʙᴏᴛ.

🚫 ɪ ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴋɪɴᴅs ᴏғ ʟɪɴᴋs ғʀᴏᴍ ᴛʜᴇ ᴄʜᴀᴛ.
⚠️ ᴜsᴇʀs ᴡɪᴛʜ ʟɪɴᴋs ɪɴ ᴛʜᴇɪʀ ʙɪᴏ ᴡɪʟʟ ʙᴇ ʀᴇsᴛʀɪᴄᴛᴇᴅ.

🔒 ʙɪᴏʟɪɴᴋ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴsᴛᴀɴᴛʟʏ.
"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [InlineKeyboardButton("📖 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="show_help")],
    [
        InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url="https://t.me/kirti_supprot_group"),
        InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Kirti_update")
    ],
    [InlineKeyboardButton("👑 ᴏᴡɴᴇʀ", url="https://t.me/Kirti_update")]
])

PRIVATE_START_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔐 ᴘʀɪᴠᴀᴛᴇ sᴛᴀʀᴛ", url=f"https://t.me/{BOT_USERNAME}?start=help")]
])

@app.on_message(filters.command("start") & (filters.private | filters.group))
async def start_command(_, message: Message):
    user = message.from_user
    chat = message.chat

    await add_user(user.id)
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await add_chat(chat.id)

    if chat.type == ChatType.PRIVATE:
        await message.reply_photo(
            photo=START_IMG,
            caption=get_start_caption(user),
            has_spoiler=True,
            reply_markup=START_BUTTONS
        )
    else:
        await message.reply_text(
            f"**ʜᴇʏ {user.mention}, ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ!**",
            reply_markup=PRIVATE_START_BUTTON
        )

@app.on_callback_query(filters.regex("^back_to_start$"))
async def back_to_start(_, query: CallbackQuery):
    user = query.from_user
    chat_id = query.message.chat.id

    await query.message.delete()  # पुराना मैसेज हटाएं

    await app.send_photo(
        chat_id=chat_id,
        photo=START_IMG,
        caption=get_start_caption(user),
        has_spoiler=True,
        reply_markup=START_BUTTONS
    )
