import telegram
import asyncio
from datetime import datetime

TOKEN = "<>"
chat_id = "<>"
date_format = "%H:%M %d-%m-%Y"
status_file = "/home/ubuntu/bin/status.file"
curr_time = datetime.now().strftime(date_format)
with open(status_file, mode="rt", encoding="utf-8") as file:
    prew_time = file.read().strip()
with open(status_file, mode="wt", encoding="utf-8") as file:
    file.write(curr_time)

delta = datetime.strptime(curr_time, date_format) - datetime.strptime(prew_time, date_format)
warn = 'WARNING' if delta.seconds > 60 else ''
bot = telegram.Bot(token=TOKEN)

async def send_message(text, chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)

async def main():
    async with bot:
        await send_message(text=f"{curr_time} delta:[{delta.seconds}] {warn}", chat_id=chat_id)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        pass
