import telebot

from config import TOKEN, keys
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


# определяем команды для взаимодействия с ботом
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = "Чтобы начать работу введите команду боту: \n <имя валюты><в какую валюту перевести \
    <количество валюты >\n Названия валют необходимо вводить как в списке.\nСписок всех доступных валют: /values"
    bot.reply_to(message, text)


# определяем команду для вывода информации по валютным парам
@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Список валют для расчета"
    for key in keys.keys():
        text = text + f'\n{key}'
    text = text + "\nвалюту необходимо указывать как в списке. "
    bot.reply_to(message, text)


# обрабатываем  текстовый тип контента и возвращаем результата в сообщении
@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        valuess = message.text.split(" ")
        if len(valuess) != 3:
            raise ConvertionException("количество переменных не равно 3, введите значения согласно инструкции. /help")

        quote, base, amount = valuess
        # если количество элементов равняется 3 вызываем функцию для конвертации
        total_changer = CurrencyConverter.convert(quote, base, amount)
        # В случае ошибки во время обработки параметров выводим ее
    except ConvertionException as e:
        bot.reply_to(message, str(e))
        # в случае ошибки на стороне сайта. Выводим информацию
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
        # если ошибок нет формируем и выводим окончательный результат расчета
    else:
        text = f'Цена {amount} {quote} в {base} - {total_changer}'
        bot.send_message(message.chat.id, text)


bot.polling()
