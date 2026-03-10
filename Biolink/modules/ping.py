import time
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Biolink import Biolink as app
from config import BOT_USERNAME

start_time = time.time()


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        remainder, result = divmod(int(seconds), 60 if count < 2 else 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
        count += 1

    for i in range(len(time_list)):
        ping_time += str(time_list[i]) + time_suffix_list[i] + " "
    return ping_time.strip()

@app.on_message(filters.command("ping", prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def ping_command(_, message: Message):
    start = time.time()
    reply = await message.reply_text("🏓")
    end = time.time()
    speed = round((end - start) * 1000)
    uptime = get_readable_time(time.time() - start_time)

    buttons = [
        [
            InlineKeyboardButton("• ᴜᴘᴅᴀᴛᴇ •", url="https://t.me/Kirti_update")
        ]
    ]

    await reply.edit_text(
        f"**ʜᴇʏ! ɪ ᴀᴍ ᴀʟɪᴠᴇ ᴀɴᴅ ᴋɪᴄᴋɪɴɢ!**\n\n"
        f"**⇝ ᴘɪɴɢ:** `{speed} ms`\n"
        f"**⇝ ᴜᴘᴛɪᴍᴇ:** `{uptime}`\n"
        f"**⇝ ʙᴏᴛ: @{BOT_USERNAME}**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
