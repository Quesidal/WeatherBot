import telegram
from Weather import weather_now, ref_forcast, weather_five
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from Wallpaper import rand_wallpaper

from keys import BOT_TOKEN

# обработчик событий = event handler = eh
bot = telegram.Bot(token=BOT_TOKEN)

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher


def eh_start(bot, update):
    """ф-я вызываемая при вводе команды /start
        выводит информацию и клавиатуру с действиями"""
    custom_keyboard = [['5 дней'], ['Завтра'], ['Дропнуть картинку']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    username = update['message']['chat']['username']
    print(username)

    bot.send_message(chat_id=update.message.chat_id,
                     text="Добрейший вечерок " + username + "\n" +
                          "Могу показать прогноз погоды в ЗП или случайную картинку с Unsplash.\n"+
                          "Это супер разработки by Quesidal",
                     reply_markup=reply_markup)


def eh_weather(bot, update):
    """ф-я вызываемая при вводе команды /weather
    выводит погоду на сегодня"""
    out = ref_forcast(weather_now())
    bot.send_message(chat_id=update.message.chat_id, text=out)


def eh_weather_five(bot, update):
    """выводит прогноз на 5 дней в виде сообщения, с клавиатурой для переключения между днями"""
    forecast = weather_five()

    day = forecast[0]

    keyboard = [[telegram.InlineKeyboardButton(forecast[0]['day'], callback_data='0'),
                 telegram.InlineKeyboardButton(forecast[1]['day'], callback_data='1'),
                 telegram.InlineKeyboardButton(forecast[2]['day'], callback_data='2'),
                 telegram.InlineKeyboardButton(forecast[3]['day'], callback_data='3'),
                 telegram.InlineKeyboardButton(forecast[4]['day'], callback_data='4')]]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    out_info ="Погода на " + day['day'] + '\n' + ref_forcast(day)
    bot.send_message(chat_id=update.message.chat_id, text=out_info, reply_markup = reply_markup)


def day_selecter_keyboard(bot, update):
    """создает клавиатуру для выбора одного из 5 дней"""
    query = update.callback_query

    forecast = weather_five()
    i = int(query.data)
    day = forecast[i]

    keyboard = [[telegram.InlineKeyboardButton(forecast[0]['day'], callback_data='0'),
                 telegram.InlineKeyboardButton(forecast[1]['day'], callback_data='1'),
                 telegram.InlineKeyboardButton(forecast[2]['day'], callback_data='2'),
                 telegram.InlineKeyboardButton(forecast[3]['day'], callback_data='3'),
                 telegram.InlineKeyboardButton(forecast[4]['day'], callback_data='4')]]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    out_info = "Погода на " + day['day'] + '\n' + ref_forcast(day)

    bot.edit_message_text(text=out_info,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id, reply_markup = reply_markup)


def eh_wallpaper(bot, update):
    """выдает случайную картинку с Unsplash"""
    bot.sendPhoto(chat_id=update.message.chat_id, photo=rand_wallpaper())


def eh_echo(bot, update):
    """обработчик сообщений"""
    username = update['message']['chat']['username']
    print(username + '   Send: ' + update.message.text)
    if update.message.text == 'Завтра':
        eh_weather(bot, update)
    elif update.message.text == '5 дней':
        eh_weather_five(bot, update)
    elif update.message.text == 'Дропнуть картинку':
        eh_wallpaper(bot, update)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Слишком много хочешь, такое еще не напрограмировано")


# связываем функции с событиями
start_handler = CommandHandler('start', eh_start)
msg_handler = MessageHandler(Filters.text, eh_echo)


# добавляем события для отслеживания
dispatcher.add_handler(msg_handler)
dispatcher.add_handler(start_handler)
# добавляем отслеживания нажатия inline клавиатуры
updater.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(day_selecter_keyboard))

print('Bot started')
# включаем отслеживание
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()

