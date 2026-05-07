import telebot
import time
import random

# --- الإعدادات (التوكن الجديد) ---
TOKEN = '8434440471:AAHmWZmlCczRnn8SlRkzD9amncDSNsU0g'
bot = telebot.TeleBot(TOKEN)

# --- روابط صور الرادار الملكي ---
IMG_WELCOME = "https://img.freepik.com/free-vector/abstract-background-design_1297-73.jpg" 
IMG_SIGNAL = "https://img.freepik.com/free-photo/view-3d-rocket-launch_23-2150703960.jpg"
IMG_WARNING = "https://img.freepik.com/free-vector/caution-background-design_1159-2911.jpg"

history = []

def analyze_pattern(data):
    if not data: return None, "📡 أرسل أول نتيجة للبدء..."
    last = data[-1]
    
    # إشارة ذهبية إذا كانت النتيجة الأخيرة منخفضة جداً
    if last < 1.30:
        target = round(random.uniform(2.20, 3.80), 2)
        return "signal", f"🔥 **إشارة ذهبية من رادار موسى!**\n\n🎯 التوقع القادم: `{target}x`\n🚀 ادخل الآن بقوة!"
    
    # تحذير تصفير إذا كانت النتيجة الأخيرة عالية جداً
    elif last > 5.00:
        target = round(random.uniform(1.00, 1.20), 2)
        return "warning", f"⚠️ **تحذير: منطقة خطر!**\n\n📉 التوقع: `{target}x`\n🚫 انتظر ولا تدخل الآن!"
    
    # نمط عادي
    else:
        target = round(last * 1.15, 2)
        if target > 2.0: target = round(random.uniform(1.5, 2.0), 2)
        return "normal", f"📊 **نمط مستقر:**\n\n🎯 التوقع: `{target}x`"

@bot.message_handler(commands=['start'])
def welcome(message):
    try: 
        bot.send_photo(message.chat.id, IMG_WELCOME, caption="👑 **أهلاً بك في رادار موسى الملكي**\n\nأرسل أرقام الجولات السابقة فوراً للتحليل.", parse_mode='Markdown')
    except: 
        bot.reply_to(message, "👑 رادار موسى الملكي جاهز!")

@bot.message_handler(func=lambda message: True)
def process(message):
    global history
    try:
        val = float(message.text)
        history.append(val)
        loading = bot.reply_to(message, "🔍 جاري فحص الرادار...")
        time.sleep(1)
        
        status, response = analyze_pattern(history)
        bot.delete_message(message.chat.id, loading.message_id)
        
        if status == "signal": 
            bot.send_photo(message.chat.id, IMG_SIGNAL, caption=response, parse_mode='Markdown')
        elif status == "warning": 
            bot.send_photo(message.chat.id, IMG_WARNING, caption=response, parse_mode='Markdown')
        else: 
            bot.send_message(message.chat.id, response, parse_mode='Markdown')
            
    except ValueError:
        bot.reply_to(message, "❌ يا موسى أرسل أرقام فقط (مثال: 1.55)")

if __name__ == "__main__":
    bot.polling(none_stop=True)
