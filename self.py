from telethon import TelegramClient, events
import requests
import re

# ← اطلاعات خودتو اینجا وارد کن
api_id = 18599862     # ← API ID
api_hash = 'db2e91d3112917b60ebc9225590a2751'  # ← API HASH
session_name = 'userbot'  # ← فایل نشست

client = TelegramClient(session_name, api_id, api_hash)

# 🔌 دریافت قیمت دلار
def get_dollar_price():
    try:
        res = requests.get("https://api.tgju.online/v1/convertor/usd")
        data = res.json()
        price = int(data['data']['price'])  # قیمت به ریال
        price_toman = price // 10
        return f"💵 قیمت روز دلار: {price_toman:,} تومان"
    except:
        return "❌ خطا در دریافت قیمت دلار."

# 📌 وقتی پیامی فرستادی
@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    text = event.raw_text.lower()

    # دستور دلار
    if re.search(r"دلار", text):
        await event.reply(get_dollar_price())

    # دستور سنجاق
    elif text.strip() == "سنجاق" and event.is_reply:
        reply = await event.get_reply_message()
        try:
            await client.pin_message(event.chat_id, reply.id)
            await event.reply("📌 پیام سنجاق شد.")
        except:
            await event.reply("❌ خطا در سنجاق کردن پیام.")

    # دستور پاک
    elif text.strip() == "پاک" and event.is_reply:
        reply = await event.get_reply_message()
        try:
            await reply.delete()
            await event.reply("🗑 پیام پاک شد.")
        except:
            await event.reply("❌ خطا در حذف پیام.")

    # دستور پاکسازی
    elif text.strip() == "پاکسازی":
        try:
            async for msg in client.iter_messages(event.chat_id, from_user="me"):
                await msg.delete()
            await event.respond("✅ همه پیام‌ها پاک شدند.")
        except:
            await event.reply("❌ خطا در پاکسازی چت.")

print("🤖 UserBot فعال شد...")
client.start()
client.run_until_disconnected()
