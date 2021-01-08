from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
import os
import json
import requests

"""
Heroku specific information
"""
# NAME = "lit-woodland-33204"

TOKEN = os.environ["TOKEN"]
PORT = os.environ.get("PORT", "5000")

updater = Updater(TOKEN)
dp = updater.dispatcher

def start(bot, update):
    reply = "Hello " + str(update.message.from_user.username) + "! \n The available functions are: \n /start to start the bot\n/tiles to see all tiles, or to find tiles by suits\n/rules for rules in Mahjong, including ways to win"
    bot.send_message(chat_id = update.message.chat_id, text=reply)

start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)

# Other commands

def rules(bot, update):
    reply = "In Mahjong, there are many ways to win. Some of the basic ones are: \n \
               1) Ping Hu\n \
               2) Peng Peng Hu\n \
               3) Qing Yi Se\n \
               4) Hun Yi Se \nWhich one do you want to know about?"
    bot.send_message(chat_id=update.message.chat_id, text=reply)

rules_handler = CommandHandler('rules', rules)
dp.add_handler(rules_handler)

def win(bot, update):
    reply = "Here are 4 main ways to win in Mahjong, which would you like to know about?"

    keyboard = [
        [ "Ping Hu", "Peng Peng Hu"],
        [ "Qing Yi Se", "Hun Yi Se"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=reply_markup)
    # bot.send_message(chat_id=update.message.chat_id, text="", reply_markup=ReplyKeyboardRemove(remove_keyboard=True, selective=False))

win_handler = CommandHandler('win', win)
dp.add_handler(win_handler)

def tiles(bot, update):
    reply = "Here is a list of all the tiles in Mahjong! Choose what *suit(e)s* your interest!"
    bot.send_message(chat_id=update.message.chat_id, text=reply)
    bot.send_photo(chat_id=update.message.chat_id, photo="https://raw.githubusercontent.com/tirameshu/MahjongMaster/master/photos/tiles.jpg")

tiles_handler = CommandHandler('tiles', tiles)
dp.add_handler(tiles_handler)


# normal functions
def pinghu_reply(bot, chat_id):
    bot.send_photo(chat_id=chat_id, photo="https://raw.githubusercontent.com/tirameshu/Mahjong_Master_python/master/photos/pinghu.png")
    reply = "Above is an example of the Ping Hu (平胡) hand.\n \
    Requirements:\n \
    1) All *sets* must be sequential. No 3 of a kind.\n \
    2) No honour tiles that can give multipliers, including winds.\n \
    3) Waiting hand must be able to win with **at least** 2 different tiles.\n \
    The hand below is not Ping Hu:"
    return reply

def pengpenghu_reply(bot, chat_id):
    bot.send_photo(chat_id=chat_id, photo="https://raw.githubusercontent.com/tirameshu/Mahjong_Master_python/master/photos/pengpenghu.png")
    reply = "Above is an example of the Peng Peng Hu (碰碰胡) hand.\n \
    Requirement:\n \
    1) All *sets* must strictly be 3 (or 4) of a kind.\n \
    The two sets on the side in the example are gang (杠, 4 of a kind) and peng (碰, 3 of a kind, one of which is the discard of another player)."
    return reply

def qingyise_reply(bot, chat_id):
    bot.send_photo(chat_id=chat_id, photo="https://raw.githubusercontent.com/tirameshu/Mahjong_Master_python/master/photos/qingyise.png")
    reply = "Above is an example of the Qing Yi Se (清一色) hand\n \
    Requirement:\n \
    1) All *tiles* must be of the same suite. The sets can be a mix of sequential and 3 (or 4) of a kind."
    return reply

def hunyise_reply(bot, chat_id):
    bot.send_photo(chat_id=chat_id, photo="https://raw.githubusercontent.com/tirameshu/Mahjong_Master_python/master/photos/hunyise.png")
    reply = "Above is an example of the Hun Yi Se (混一色) hand\n \
    Requirement:\n \
    1) *Tiles* must be of the same suite + honour tiles. The sets can be a mix of sequential and 3 (or 4) of a kind. \n \
    The honour tiles can be either for the eyes (pair) or a set."
    return reply

# General text responses
def respond(bot, update):
    text = update.message.text
    chat_id = update.message.chat_id

    if text.lower() == "ping hu":
        reply = pinghu_reply(bot, chat_id)
        bot.send_message(chat_id=chat_id, text=reply)
        bot.send_photo(chat_id=chat_id,
                       photo="https://raw.githubusercontent.com/tirameshu/Mahjong_Master_python/master/photos/not%20pinghu.png")

    elif text.lower() == "peng peng hu":
        reply = pengpenghu_reply(bot, chat_id)
        bot.send_message(chat_id=chat_id, text=reply)

    elif text.lower() == "qing yi se":
        reply = qingyise_reply(bot, chat_id)
        bot.send_message(chat_id=chat_id, text=reply)

    elif text.lower() == "hun yi se":
        reply = hunyise_reply(bot, chat_id)
        bot.send_message(chat_id=chat_id, text=reply)

    else:
        reply = "Sorry! I can't really converse yet :("
        bot.send_message(chat_id=chat_id, text=reply)

respond_handler = MessageHandler(Filters.text, respond)
dp.add_handler(respond_handler)

# when 'Tong', 'Dots'
#     reply = "Here is a list of dotted tiles 筒子 in ascending order!"
#     #bot.api.send_photo(chat_id: message.chat.id, photo:
#      #   Faraday::UploadIO.new('/Users/mandy/Repos/MahjongMaster/photos/dots.jpg', 'image/jpeg'))
#     bot.api.send_message(chat_id: person_id, text: reply)
# when 'Tiao/Suo', 'Tiao', 'Suo', 'Bamboos'
#     reply = "Here is a list of bamboo tiles 条子/ 索子 in ascending order!"
#     #bot.api.send_photo(chat_id: message.chat.id, photo:
#      #   Faraday::UploadIO.new('/Users/mandy/Repos/MahjongMaster/photos/bamboos.jpg', 'image/jpeg'))
#     bot.api.send_message(chat_id: person_id, text: reply)
# when 'Wan', 'Characters'
#     reply = "Here is a list of character tiles 萬子 in ascending order!"
#     #bot.api.send_photo(chat_id: message.chat.id, photo:
#      #   Faraday::UploadIO.new('/Users/mandy/Repos/MahjongMaster/photos/characters.jpg', 'image/jpeg'))
#     bot.api.send_message(chat_id: person_id, text: reply)
# when 'DaPai', 'Honours'
#     reply = "Here is a list of honour tiles 大牌 in no particular order!"
#     #bot.api.send_photo(chat_id: message.chat.id, photo:
#      #   Faraday::UploadIO.new('/Users/mandy/Repos/MahjongMaster/photos/honours.jpg', 'image/jpeg'))
#     bot.api.send_message(chat_id: person_id, text: reply)

# start webhooks
updater.start_webhook(listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN)
updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
updater.idle()
