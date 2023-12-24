import telebot 
from config import token
from random import randint

from logic import Pokemon,Wizard,Fighter

bot = telebot.TeleBot(token) 
@bot.message_handler(commands=['info'])
def info_pok(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pok.info())
@bot.message_handler(commands=['go'])
def start(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        
        chance = randint(1,3)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        if chance == 2:
            pokemon = Wizard(message.from_user.username)
            bot.send_message(message.chat.id,"Wizard")
        if chance == 3:
            pokemon = Fighter(message.from_user.username)
            bot.send_message(message.chat.id,"Fighter")

        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['attack'])
def attack(message):
    if message.reply_to_message:
        if message.from_user.username in Pokemon.pokemons.keys() and message.reply_to_message.from_user.username in Pokemon.pokemons.keys():
            pok = Pokemon.pokemons[message.from_user.username]
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id,res)
        else:
            bot.send_message(message.chat.id, "You can't attack people. Either you or them don't have a pokemon!")
    else:
        bot.send_message(message.chat.id, "Reply to a message first.")

@bot.message_handler(commands=['compare'])
def compare(message):
    if message.reply_to_message:
        if message.from_user.username in Pokemon.pokemons.keys() and message.reply_to_message.from_user.username in Pokemon.pokemons.keys():
            pok = Pokemon.pokemons[message.from_user.username]
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            if pok < enemy:
                bot.reply_to(message,"You have less health than your enemy!")
            elif pok > enemy:
                bot.reply_to(message,"You have more health than your enemy!")
            else:
                bot.reply_to(message,"You two have the same amount of health")
        else:
            bot.send_message(message.chat.id, "You can't compare Pokemons. Either you or them don't have a pokemon!")
    else:
        bot.send_message(message.chat.id, "Reply to a message first.")
bot.infinity_polling(none_stop=True)
