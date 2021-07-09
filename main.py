# Made with python3
# (C) @FayasNoushad
# Copyright permission under GNU General Public License v3.0
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Telegraph-Uploader-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import upload_file

FayasNoushad = Client(
    "Telegraph Uploader Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")

START_TEXT = """
Hello {}, 

`I am an under 5MB media or file to telegra.ph link uploader bot`.

👲 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : [ʙx ʙᴏᴛᴢ](https://t.me/BX_Botz)
"""
HELP_TEXT = """
- Just give me a media under 5MB
- Then I will download it
- I will then upload it to the telegra.ph link

👲 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : [ʙx ʙᴏᴛᴢ](https://t.me/BX_Botz)
"""
ABOUT_TEXT = """
- **Bot :** `Telegraph Uploader`
- **Creator :** [ᴍʜᴅ ᴍᴜꜰᴀᴢ](https://telegram.me/Mufaz123)
- **Channel :** [ʙx ʙᴏᴛᴢ](https://telegram.me/BX_Botz)
- **Source :** [Click here](https://t.me/nokiyirunnoippokitum)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)
- **Server :** [Heroku](https://heroku.com)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🤖 Bot Updates', url='https://telegram.me/BX_Botz'),
        InlineKeyboardButton('👥Support Group', url='https://telegram.me/BXSupport')
        ],[
        InlineKeyboardButton('⚙️Help', callback_data='help'),
        InlineKeyboardButton('🔒Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏠Home', callback_data='home'),
        InlineKeyboardButton('🔰About', callback_data='about'),
        InlineKeyboardButton('🔒Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏠Home', callback_data='home'),
        InlineKeyboardButton('⚙️Help', callback_data='help'),
        InlineKeyboardButton('🔒Close', callback_data='close')
        ]]
    )

@FayasNoushad.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()
    

@FayasNoushad.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        quote=True,
        reply_markup=reply_markup
    )

@FayasNoushad.on_message(filters.private & filters.media)
async def getmedia(bot, update):
    medianame = DOWNLOAD_LOCATION + str(update.from_user.id)
    try:
        message = await update.reply_message(
            text="`Processing...`",
            quote=True,
            disable_web_page_preview=True
        )
        await bot.download_media(
            message=update,
            file_name=medianame
        )
        response = upload_file(medianame)
        try:
            os.remove(medianame)
        except:
            pass
    except Exception as error:
        print(error)
        text=f"Error :- <code>{error}</code>"
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('🛠️Help', callback_data='help')
            ]]
        )
        await message.edit_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
        return
    text=f"**Link :-** `https://telegra.ph{response[0]}`\n\n**Join :-** @BX_Botz"
    reply_markup=InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="📌Open Link📌", url=f"https://telegra.ph{response[0]}"),
        InlineKeyboardButton(text="⚜️Share Me⚜️", url="https://t.me/share/url?url=%2A%2AHai%20Friends%2C%20%2A%2A%0A%60Here%20We%20Found%20an%20Advanced%20Telegraph%20Uploader%20Bot%60%0ALink%20%40BXTelegraphBot%20Channel%20%40BX_Botz")
        ],[
        InlineKeyboardButton(text="🤖 Update Channel", url="https://telegram.me/BX_Botz"),
        InlineKeyboardButton(text="👥Support Group", url="https://telegram.me/BxSupport")
        ]]
    )
    await message.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

FayasNoushad.run()
