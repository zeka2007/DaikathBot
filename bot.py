import telebot
from telebot import types
import config
from meme_parser import parse_meme
from random import randint, choice

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['start'])
def start(message):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for name in config.button_names:
        reply_markup.add(types.KeyboardButton(name))
    bot.send_message(message.chat.id,
    f"Привет, **{message.from_user.first_name}**! Я бот для Телеграм, который может выполнять любые твои команды. Выбери, что ты хочешь сделать",
    reply_markup = reply_markup)
    bot.send_game(message.chat.id, 'snake_game')


@bot.message_handler(content_types = ['text'])
def answer(message):
    text = message.text
    choose = config.button_names
    if text == choose[0]:
        bot.send_message(message.chat.id,
        randint(0, 100))
    elif text == choose[2]:
        meme = parse_meme()
        inline_markup= types.InlineKeyboardMarkup()
        inline_markup.add(types.InlineKeyboardButton(text = 'Узнать больше', url = meme[1]))
        bot.send_photo(message.chat.id,
        meme[0], reply_markup = inline_markup)
    elif text == choose[3]:
        meme = parse_meme('trands')
        inline_markup= types.InlineKeyboardMarkup()
        inline_markup.add(types.InlineKeyboardButton(text = 'Узнать больше', url = meme[1]))
        bot.send_photo(message.chat.id,
        meme[0], reply_markup = inline_markup)
    elif text == choose[4]:
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        reply_markup.add(types.KeyboardButton(config.cance))
        msg = bot.send_message(message.chat.id,
        'Введите название мема:', reply_markup = reply_markup)
        bot.register_next_step_handler(msg, get_meme_name)

def get_meme_name(message):

    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)

    for name in config.button_names:
        reply_markup.add(types.KeyboardButton(name))
    if not message.text == config.cance:
        meme = parse_meme(search = message.text)
        if meme == False:
            bot.send_message(message.chat.id, 'Извините, но я не смог ничего найти 😢.',
            reply_markup = reply_markup)
        else:
            inline_markup= types.InlineKeyboardMarkup()
            inline_markup.add(types.InlineKeyboardButton(text = 'Узнать больше', url = meme[1]))
            bot.send_photo(message.chat.id,
            meme[0], reply_markup = inline_markup)
    bot.send_message(message.chat.id, 'Выберите действие из списка:',
    reply_markup = reply_markup)

@bot.message_handler(commands = ['game'])
def game(message):
    bot.send_game(message.chat.id, 'snake_game')

@bot.callback_query_handler(func = lambda call:True)
def game_query(call):
    if call.game_short_name == 'snake_game':
        bot.answer_callback_query(call.id, url = 'https://maxizhukov.github.io/telegram_game_front/')
        bot.set_game_score(call.from_user.id, 100, inline_message_id = call.message.id)

bot.polling(none_stop = True, interval = 0)
