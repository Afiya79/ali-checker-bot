import telebot
import requests

# Yahan apna token bina kisi space ke dalein
TOKEN = '8615792192:AAEk8e6iQmmaiBVT8y592FWR944AacZeSgA' 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome Ali! Card number bhejien uski info nikalne ke liye.")

@bot.message_handler(func=lambda message: True)
def get_card_info(message):
    # User ke msg se spaces hata dena
    card_num = message.text.replace(" ", "")
    
    if len(card_num) < 6:
        bot.reply_to(message, "❌ Kam se kam 6 digit bhejien.")
        return

    # Card details nikalne ke liye BIN Lookup
    bin_num = card_num[:6]
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_num}")
        
        if response.status_code == 200:
            data = response.json()
            bank = data.get('bank', {}).get('name', 'N/A')
            scheme = data.get('scheme', 'N/A')
            brand = data.get('brand', 'N/A')
            country = data.get('country', {}).get('name', 'N/A')
            
            info = (f"🔍 **Card Info Found**\n\n"
                    f"🏦 Bank: {bank}\n"
                    f"💳 Type: {scheme.upper()} {brand}\n"
                    f"🌍 Country: {country}")
            bot.reply_to(message, info, parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Is card ki details nahi mili.")
    except:
        bot.reply_to(message, "⚠️ Server error, thodi der baad try karein.")

bot.polling()
