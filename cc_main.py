import telebot
from config import keys, TOKEN, text_help
from extensions import ConvertationException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет!\n Я Бот-Конвертер валют. Я умею делать следующее:\n' + text_help
    bot.reply_to(message, text)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = text_help
    bot.reply_to(message, text)


# Обработчик команды '/values' - список валют доступных для конвертации:
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


# Запрос на конвертацию:
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertationException('Неверное количество параметров!')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)

    except ConvertationException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду!\n {e}')
    else:
        text = f'Цена покупки {amount} {quote}  -  {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

