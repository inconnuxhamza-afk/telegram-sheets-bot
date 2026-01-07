import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys

# 1. إعدادات Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)
    
    # اختبار: واش البوت كيشوف الجدول؟
    all_sheets = client.openall()
    print(f"🔍 البوت لقى {len(all_sheets)} جداول فـ الحساب ديالو.")
    for s in all_sheets:
        print(f"📋 جدول متاح: {s.title}")

    # محاولة فتح الجدول بالـ ID
    sheet = client.open("pako_sheet").sheet1
    
    print("✅ تم الاتصال بالجدول بنجاح!")

except Exception as e:
    print(f"❌ مشكل فـ الاتصال بـ Google Sheets: {e}")
    print("💡 تأكد بلي درتي Share للإيميل اللي فـ creds.json مع الجدول.")
    sys.exit()

# 2. إعدادات Telegram Bot
TOKEN = '8540110979:AAFhp_Mfyql7acqdm3NxIZNOQlIcFnT7gcA'
bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً بك! أنا بوت تسجيل الطلبات. شنو هي سميتك الكاملة؟")
    bot.register_next_step_handler(message, process_name)

def process_name(message):
    user_id = message.from_user.id
    user_data[user_id] = {'name': message.text}
    bot.reply_to(message, f"متشرفين يا {message.text}! صيفط رقم الهاتف ديالك؟")
    bot.register_next_step_handler(message, process_phone)

def process_phone(message):
    user_id = message.from_user.id
    user_data[user_id]['phone'] = message.text
    bot.reply_to(message, "شنو هو الطلب ديالك؟")
    bot.register_next_step_handler(message, process_order)

def process_order(message):
    user_id = message.from_user.id
    try:
        name = user_data[user_id]['name']
        phone = user_data[user_id]['phone']
        order = message.text
        sheet.append_row([name, phone, order])
        bot.reply_to(message, "✅ المعلومات تقيدات بنجاح!")
        print(f"✅ طلب جديد من {name}")
    except Exception as e:
        bot.reply_to(message, "❌ خطأ فـ التسجيل.")
        print(f"Error: {e}")

print("🚀 الماكينة ناضية.. جرب دير /start")
bot.polling()