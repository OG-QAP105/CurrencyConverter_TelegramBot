import telebot
from config import keys, TOKEN
from extensions import ConvertationException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для конвертации введите команду в формате\n (в одну строку через пробел):\n' \
           '\n<имя покупаемой валюты>  <имя валюты за которую покупаем>  <кол-во покупаемой валюты>\n ' \
           '\nКоманды:' \
           '\n/values - посмотреть список доступных валют.' \
           '\n/start или /help - получить помощь\n'
    bot.reply_to(message, text)

# Обрабатчик команды '/values' - список валют доступных для конвертации:
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


bot.polling()


