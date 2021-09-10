import telebot
import API

TOKEN = "1981693853:AAFRnv0lslpX7lrsCl-Qu6C_eXhcBUoDJBw"

bot = telebot.TeleBot(TOKEN)
base_currency = "EUR"
needed_currency = "CAD"

@bot.message_handler(commands=['start','hello'])
def start_bot(message):
    bot.reply_to(message, "Hello!")

@bot.message_handler(commands=['list','lst'])
def currency_list(message):
    rate_dictionary = API.currency_rate_list(base_currency)
    rate_message = f'{base_currency}-rate:\n'
    for currency, rate in rate_dictionary.items():
        rate_message += currency + " : " + str(rate) + "\n"
    bot.send_message(message.from_user.id, rate_message)

@bot.message_handler(commands=['exchange','exchange_EUR'])
def ask_currency(message):
    bot.send_message(message.from_user.id, "To what currency you want exchange EUR?")
    bot.register_next_step_handler(message, ask_quantity)

def ask_quantity(message):
    if API.check_currency(message.text):
        global needed_currency
        needed_currency = message.text
        bot.send_message(message.from_user.id, "How many EUR do you want to exchange?")
        bot.register_next_step_handler(message, exchange_EUR_to)
    else:
        bot.send_message(message.from_user.id, "Sorry, but we don`t support this currency. Try again!\n"
                                               "To what currency you want exchange EUR?")
        bot.register_next_step_handler(message, ask_quantity)

def exchange_EUR_to(message):
    exchanged_rate = API.exchange_to(float(message.text),base_currency, needed_currency )
    bot.send_message(message.from_user.id, "It will be - " + str(round(exchanged_rate,2)))

@bot.message_handler(commands=["history"])
def show_last_7_days_EUR_TARGET_rate(message):
    bot.send_message(message.from_user.id, "Euro chart to which currency do you want to see?")
    bot.register_next_step_handler(message, show_EUR_plot)

def show_EUR_plot(message):
    if API.check_currency(message.text):
        bot.send_message(message.from_user.id, "Wait a minute...")
        API.get_last_7_days_EUR_CAD_info(message.text)
        bot.send_photo(message.from_user.id, photo=open("plot.png", "rb"))
    else:
        bot.send_message(message.from_user.id, "Sorry, but we don`t support this currency. Try another !")
        bot.register_next_step_handler(message, show_last_7_days_EUR_TARGET_rate)


bot.polling()