# Бот переводчик, переводит с русского на английский и со всех на русский.
# Библиотеки (pip install googletrans==3.1.0a0 ,
#             pip install pyTelegramBotAPI,
#             pip install asyncio).

## Импорт библиотек
from googletrans import Translator
from telebot.async_telebot import AsyncTeleBot
import asyncio

# Апи бота нужно получить у @BotFather в Телеграме.
bot = AsyncTeleBot("API_bot", parse_mode=None)

# Обработка команды /start приветствие.
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message,'------\n'
                 + 'Здравствуй, '
                 + message.from_user.first_name
                 + ' \nПереведу с русского на английский \nИ с других языков на русский '
                 +'\n------')

# Обработка команды /help.
@bot.message_handler(commands=['help'])
async def send_welcome(message):
    await bot.reply_to(message,'------\n'
                 + 'Просто вводи текст и нажимай отправить\n'
                 + 'Я сам определю какой это язык\n'
                 + 'Если не перевел, попробуй еще раз\n'
                 + 'Перевод гугл'
                 +'\n------')

# Обработка текста сообщения, если ввод на русском, то перевод на английский,
# если другой язык, то перевод на русский.
@bot.message_handler()
async def user_text(message):
    translator = Translator()

    # Определение языка ввода.
    lang = translator.detect(message.text)
    lang = lang.lang

    # Если ввод по русски, то перевести на английский по умолчанию.
    if lang == 'ru':
        send = translator.translate(message.text)
        await bot.reply_to(message, '------\n'+ send.text +'\n------')

    # Иначе другой язык перевести на русский {dest='ru'}.
    else:
        send = translator.translate(message.text, dest='ru')
        await bot.reply_to(message, '------\n'+ send.text +'\n------')


# Запуск и повторение запуска при сбое.
asyncio.run(bot.infinity_polling())

