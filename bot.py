# Бот переводчик, переводит с русского на английский и со всех на русский.
# Для начала необходимо установить библиотеки 
#             sudo apt install pip
#             pip install googletrans==3.1.0a0  -важно утановить именно эту версию библиотеки
#             pip install pyTelegramBotAPI
#             pip install asyncio
#             pip install aiohttp

## Импорт библиотек
from googletrans import Translator
from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import InlineQuery, InputTextMessageContent
from telebot import types

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
    # Если нужен другой язык, измени <message.text> на <message.text, dest='нужный язык'>.
    if lang == 'ru':
        send = translator.translate(message.text)
        await bot.reply_to(message, '------\n'+ send.text +'\n------')

    # Иначе другой язык перевести на русский {dest='ru'}.
    else:
        send = translator.translate(message.text, dest='ru')
        await bot.reply_to(message, '------\n'+ send.text +'\n------')

# Обработка картинок с подписями
@bot.message_handler(content_types=['photo'])
async def handle_image(message):
    translator = Translator()
    #Обработчик сообщений с изображениями
    chat_id = message.chat.id
    photo = message.photo[-1].file_id
    caption = message.caption

    # Определение языка ввода.
    lang = translator.detect(caption)
    lang = lang.lang

    # Если подпись по русски, то перевести на английский по умолчанию.
    if lang == 'ru':
        send = translator.translate(caption)

    # Иначе другой язык перевести на русский {dest='ru'}.
    else:
        send = translator.translate(caption, dest='ru')
        
    
    await bot.send_photo(chat_id, photo, caption=send.text)



# Обработка инлайн запросов
@bot.inline_handler(lambda query: True)
async def inline_query(query):
    results = []
    translator = Translator()
    text = query.query.strip()

    # Если запрос пустой, не делаем перевод
    if not text:
        return

    # Определение языка ввода.
    lang = translator.detect(text)
    lang = lang.lang

    # Если ввод по русски, то перевести на английский по умолчанию.
    if lang == 'ru':
        send = translator.translate(text)
        results.append(types.InlineQueryResultArticle(
            id='1', title=send.text, input_message_content=types.InputTextMessageContent(
                message_text=send.text)))

    # Иначе другой язык перевести на русский {dest='ru'}.
    else:
        send = translator.translate(text, dest='ru')
        results.append(types.InlineQueryResultArticle(
            id='1', title=send.text, input_message_content=types.InputTextMessageContent(
                message_text=send.text)))

    await bot.answer_inline_query(query.id, results)

# Запуск и повторение запуска при сбое.
asyncio.run(bot.infinity_polling())

