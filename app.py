import telebot
import time
import random

# --- الإعدادات الأساسية ---
TOKEN = '8692440137:AAGp0hzZQ0raZez6DVwYXiZOr4z_8qGZK-U'
bot = telebot.TeleBot(TOKEN)

# --- روابط الصور الملكية ---
IMG_WELCOME = "https://img.freepik.com/free-vector/abstract-background-design_1297-73.jpg" 
IMG_SIGNAL = "https://img.freepik.com/free-photo/view-3d-rocket-launch_23-2150703960.jpg"
IMG_WARNING = "https://img.freepik.com/free-vector/caution-background-design_1159-2911.jpg"

history = []

def analyze_pattern(data):
    if not data: return None, "📡 أرسل أول نتيجة..."
    last = data[-1]
    if last < 1.30:
        target = round(random.uniform(2.10, 3.50), 2)
        return "signal", f"🔥 **إشارة ذهبية!**\n\n🎯 التوقع: `{target}x`\n🚀 ادخل الآن!"
    elif last > 4.50:
        target = round(random.uniform(1.01, 1.25), 2)
        return "warning", f"⚠️ **تحذير: تصفير!**\n\n📉 التوقع: `{target}x`\n🚫 لا تدخل!"
    else:
        target = round(last * 1.12, 2)
        return "normal", f"📊 **نمط مستقر:**\n\n🎯 التوقع: `{target}x`"

@bot.message_handler(commands=['start'])
def welcome(message):
    try: bot.send_photo(message.chat.id, IMG_WELCOME, caption="👑 رادار موسى الملكي جاهز!", parse_mode='Markdown')
    except: bot.reply_to(message, "👑 رادار موسى الملكي جاهز!")

@bot.message_handler(func=lambda message: True)
def process(message):
    global history
    try:
        val = float(message.text)
        history.append(val)
        loading = bot.reply_to(message, "🔍 جاري التحليل...")
        time.sleep(1)
        status, response = analyze_pattern(history)
        bot.delete_message(message.chat.id, loading.message_id)
        if status == "signal": bot.send_photo(message.chat.id, IMG_SIGNAL, caption=response, parse_mode='Markdown')
        elif status == "warning": bot.send_photo(message.chat.id, IMG_WARNING, caption=response, parse_mode='Markdown')
        else: bot.send_message(message.chat.id, response, parse_mode='Markdown')
    except: bot.reply_to(message, "❌ أرسل أرقام فقط")

if __name__ == "__main__":
    bot.polling(none_stop=True)
