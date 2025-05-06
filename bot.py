
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp

API_ID = 21070919  # Replace with your API ID
API_HASH = "1a70e1253cc7009c1bea592d4f62e707"  # Replace with your API Hash
BOT_TOKEN = "7730974471:AAHfUyJaLWGIUA-mrbfWc9hyFCKpu_GLuPk"
FORCE_JOIN = "malwareReapers"  # without @

app = Client("yt_download_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def is_joined(client, user_id):
    try:
        member = await client.get_chat_member(FORCE_JOIN, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@app.on_message(filters.command("start"))
async def start(client, message):
    if not await is_joined(client, message.from_user.id):
        channel_username = "MalwareReapers"
await message.reply(f"❌ Pehle @{channel_username} channel join karo fir use karo.")
    await message.reply("👋 Welcome! Send any YouTube link to download video/audio.")

@app.on_message(filters.text & filters.private)
async def download_video(client, message: Message):
    if not await is_joined(client, message.from_user.id):
        await message.reply(f"❌ Pehle @{FORCE_JOIN} channel join karo fir use karo.",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Channel", url=f"https://t.me/{MalwareReapers}")]]))
        return

    url = message.text.strip()
    await message.reply("⏬ Downloading started... Please wait!")

    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            await message.reply_video(video=file_path, caption=f"✅ Downloaded: {info.get('title')}")
            os.remove(file_path)
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

app.run()
