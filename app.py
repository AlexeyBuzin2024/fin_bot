import telebot
from config import keys, TOKEN
from extensions import FinConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])            #Отправка инструкции по использованию бота при получении
def help(message: telebot.types.Message):                   #команд 'start', 'help'
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])                   #Отправка списка доступных валют по команде 'values'
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])               #Функционал работы бота
def convert(message: telebot.types.Message):
   try:
        values = message.text.split(' ')                           #Получение значений из сообщения пользователя

        if len(values) < 3:
            raise APIException('Слишком мало параметров')           #Отлавливание ошибки "недописанное сообщение"

        if len(values) > 3:
            raise APIException('Слишком много параметров')          #Отлавливание ошибки "лишние параметры"

        quote, base, amount = values
        total_base = FinConverter.get_price(quote, base, amount)      #получение из метода необходимого значения
   except APIException as e:                                        #разделение ошибок на:
       bot.reply_to(message, f'ошибка пользователя\n{e}')       #ошибки пользователя
   except Exception as e:
       bot.reply_to(message, f'Не удалось обработать команду\n{e}')     #ошибки сервера
   else:
       text = f'Цена {amount} {quote} в  {base} - {total_base}'     #вывод результата
       bot.send_message(message.chat.id, text)

bot.polling()