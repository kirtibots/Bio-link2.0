import time
import psutil
from time import perf_counter
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Biolink import Biolink as app
from Biolink.helper.database import get_users, get_chats, get_new_users, get_new_chats


START_TIME = time.time()


def get_uptime():
    uptime = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"


@app.on_message(filters.command("stats") & filters.private)
async def stats_handler(_, message: Message):

    start = perf_counter()

    user_data = await get_users()
    chat_data = await get_chats()
    new_users = await get_new_users()
    new_chats = await get_new_chats()

    total_users = len(user_data.get("users", []))
    total_chats = len(chat_data.get("chats", []))

    # RAM
    ram = psutil.virtual_memory()
    ram_used = round(ram.used / (1024**3), 2)
    ram_total = round(ram.total / (1024**3), 2)

    # CPU
    cpu = psutil.cpu_percent()

    # Disk
    disk = psutil.disk_usage('/')
    disk_used = round(disk.used / (1024**3), 2)
    disk_total = round(disk.total / (1024**3), 2)

    # Ping
    ping = round((perf_counter() - start) * 1000)

    text = f"""
╔══❰ 📊 **𝐔𝐋𝐓𝐑𝐀 𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐒** ❱══╗

👥 **𝐓ᴏᴛᴀʟ 𝐔sᴇʀs :** `{total_users}`
💬 **𝐓ᴏᴛᴀʟ 𝐂ʜᴀᴛs :** `{total_chats}`

🆕 **𝐍ᴇᴡ 𝐔sᴇʀs :** `{new_users}`
🆕 **𝐍ᴇᴡ 𝐂ʜᴀᴛs :** `{new_chats}`

━━━━━━━━━━━━━━━

🧠 **𝐑𝐀𝐌 :** `{ram_used} / {ram_total} GB`
⚡ **𝐂𝐏𝐔 :** `{cpu}%`
📦 **𝐃𝐢𝐬𝐤 :** `{disk_used} / {disk_total} GB`

━━━━━━━━━━━━━━━

📶 **𝐏𝐢𝐧𝐠 :** `{ping} ms`
⏱ **𝐔𝐩ᴛɪᴍᴇ :** `{get_uptime()}`

╚══════════════════╝
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔄 Refresh", callback_data="refresh_stats"),
                InlineKeyboardButton("❌ Close", callback_data="close_stats")
            ]
        ]
    )

    await message.reply_text(text, reply_markup=buttons)


@app.on_callback_query(filters.regex("close_stats"))
async def close_stats(_, query):
    await query.message.delete()


@app.on_callback_query(filters.regex("refresh_stats"))
async def refresh_stats(_, query):
    await query.answer("Refreshing Stats ⚡", show_alert=False)
    await query.message.delete()
