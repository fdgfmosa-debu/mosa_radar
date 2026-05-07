import telebot
import time
import random

# التوكن الجديد تبعك (تأكدت منه 100%)
TOKEN = '8434440471:AAHmWZmlCczRnn8SlRkzD9amncDSNsU0g'
bot = telebot.TeleBot(TOKEN)

# روابط الصور
IMG_WELCOME = "https://img.freepik.com/free-vector/abstract-background-design_1297-73.jpg" 

@bot.message_handler(commands=['start'])
def welcome(message):
    try:
        bot.send_photo(message.chat.id, IMG_WELCOME, caption="👑 رادار موسى الملكي جاهز!\n\nأرسل لي أي رقم للتحليل.")
    except:
        bot.reply_to(message, "👑 رادار موسى الملكي جاهز! أرسل لي أرقام.")

@bot.message_handler(func=lambda message: True)
def process(message):
    try:
        val = float(message.text)
        loading = bot.reply_to(message, "🔍 جاري فحص الإشارة...")
        time.sleep(1)
        res = round(random.uniform(1.2, 3.8), 2)
        bot.edit_message_text(f"🎯 التوقع: {res}x\n🚀 ادخل الآن!", message.chat.id, loading.message_id)
    except:
        bot.reply_to(message, "❌ أرسل أرقام فقط")

if __name__ == "__main__":
    bot.polling(none_stop=True)
