from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.enums import ChatType

from config import OWNER_ID, BOT_USERNAME
from Biolink import Biolink as app
from Biolink.helper.database import add_user, add_chat

START_IMG = "https://files.catbox.moe/gdjna3.jpg"

def get_start_caption(user):
    return f"""
**ʜᴇʏ** {user.mention} 🥀

🤖 I am a **Link Remover Bot**.
I delete messages with links and restrict users who have links in their bio.

🚫 I also delete messages with **biolink**.
"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("• 𝗔𝗗𝗗 𝗠𝗘 𝗕𝗔𝗕𝗬 •", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [InlineKeyboardButton("• 𝗛𝗘𝗟𝗣 𝗔𝗡𝗗 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦 •", callback_data="show_help")],
    [
        InlineKeyboardButton("• 𝗦𝗨𝗣𝗣𝗢𝗥𝗧 •", url="https://t.me/+_zR_OAMZ6iE2YTBl"),
        InlineKeyboardButton("• 𝗨𝗣𝗗𝗔𝗧𝗘 •", url="https://t.me/bot_x_worlds")
    ],
    [InlineKeyboardButton("• 𝗢𝗪𝗡𝗘𝗥 •", url="https://t.me/PerfectselIer")]
])

PRIVATE_START_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("• 𝗣𝗥𝗜𝗩𝗔𝗧𝗘 𝗦𝗧𝗔𝗥𝗧 •", url=f"https://t.me/{BOT_USERNAME}?start=help")]
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
