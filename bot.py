import telebot
import requests

# Aapka Token jo image.png mein dikha
TOKEN = '8615792192:AAEk8e6iQmma iBVT8y592FWR944AacZeSgA'
bot = telebot.TeleBot(TOKEN)

def luhn_check(card_number):
    card_number = [int(d) for d in str(card_number) if d.isdigit()]
    if not card_number: return False
    total = sum(card_number[-1::-2])
    reverse_digits = card_number[-2::-2]
    for digit in reverse_digits:
        doubled = digit * 2
        total += (doubled if doubled <= 9 else doubled - 9)
    return total % 10 == 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome Ali! Card number bhejein check karne ke liye.")

@bot.message_handler(func=lambda message: True)
def check_card(message):
    cc_num = message.text.strip()
    bin_num = cc_num[:6]
    
    if luhn_check(cc_num):
        # BIN lookup start
        res = requests.get(f"https://lookup.binlist.net/{bin_num}")
        if res.status_code == 200:
            data = res.json()
            bank = data.get('bank', {}).get('name', 'Unknown')
            result = f"✅ Valid Card!\n🏦 Bank: {bank}\n💳 Type: {data.get('type')}"
        else:
            result = "✅ Valid Structure (BIN details not found)."
    else:
        result = "❌ Invalid Card Number."
    
    bot.reply_to(message, result)

bot.polling()
