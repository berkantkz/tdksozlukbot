# TDK Sözlük bot
#
# berkantkz

# GLOBALS

import re
import discord
from telegram.utils.helpers import escape_markdown
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
import requests
import json
from uuid import uuid4
from unittest import result
import logging
import os

url = "https://sozluk.gov.tr/gts?ara="
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }
)

### TELEGRAM BOT ###

token_telegram = os.environ["TDKSOZLUKBOT_TOKEN"]

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    # update.message.reply_text('Hi!')
    print("TDK Sözlük başlatıldı")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    # update.message.reply_text('Help!')


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query == "":
        return

    print("\n\t*** TELEGRAM BOT ***")

    terim = query
    print(url + terim)
    tdk = requests.get((url + terim), headers=headers)
    veri = json.loads(tdk.text)

    if "error" in veri:
        return

    anlamlar = veri[0]["anlamlarListe"]
    lisan = "_" + veri[0]["lisan"] + "_" if veri[0]["lisan"] else "Türkçe"
    sonuc = f'**{terim}**:\n\nDil: {lisan}\n'

    if veri[0]["birlesikler"] != None:
        sonuc += "Birleşikler: " + veri[0]["birlesikler"] + "\n\n"
    else:
        sonuc += "\n"

    for i in range(len(anlamlar)):
        if "ozelliklerListe" in anlamlar[i]:
            sonuc += "_" + anlamlar[i]["ozelliklerListe"][0]["tam_adi"] + "_\n"

        sonuc += f"**{i+1}**-) `" + anlamlar[i]["anlam"] + "`\n"

        if "orneklerListe" in anlamlar[i]:
            for o in range(len(anlamlar[i]["orneklerListe"])):
                sonuc += "_Örnek:_ " + \
                    anlamlar[i]["orneklerListe"][o]["ornek"] + "\n"
                if "yazar" in anlamlar[i]["orneklerListe"][o]:
                    sonuc += "\t\t_ -" + \
                        anlamlar[i]["orneklerListe"][o]["yazar"][0]["tam_adi"] + "_\n\n"
                else:
                    sonuc += "\n"
        else:
            sonuc += "\n"

    son = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=query,
            input_message_content=InputTextMessageContent(sonuc, parse_mode=ParseMode.MARKDOWN))
    ]

    update.inline_query.answer(son)
    print("\t*** TELEGRAM BOT ***\n")


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token_telegram)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


if __name__ == '__main__':
    main()

### TELEGRAM BOT ###

### DISCORD BOT ###

token_discord = os.environ['TDKSOZLUKBOT_DISCORD']


class tdksozluk(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if not (client.user.mentioned_in(message)) or "@everyone" in message.content:
            return

        print("\n\t*** DISCORD BOT ***")

        if message.author != client.user:
            print('Message from {0.author}: {0.content}'.format(message))

        terim = re.sub("<@966110075901083648> +", "",
                       re.sub(" +", " ",  message.content))
        print(url + terim)
        tdk = requests.get((url + terim), headers=headers)
        veri = json.loads(tdk.text)

        if "error" in veri:
            return await message.reply("Aranan bu sözcük TDK'da mevcut değil.", mention_author=False)

        anlamlar = veri[0]["anlamlarListe"]
        lisan = "_" + veri[0]["lisan"] + "_" if veri[0]["lisan"] else "Türkçe"
        sonuc = f'**{terim}**:\n\nDil: {lisan}\n'

        if veri[0]["birlesikler"] != None:
            sonuc += "Birleşikler: " + veri[0]["birlesikler"] + "\n\n"
        else:
            sonuc += "\n"

        for i in range(len(anlamlar)):
            if "ozelliklerListe" in anlamlar[i]:
                sonuc += "_" + \
                    anlamlar[i]["ozelliklerListe"][0]["tam_adi"] + "_\n"

            sonuc += f"**{i+1}**-) `" + anlamlar[i]["anlam"] + "`\n"

            if "orneklerListe" in anlamlar[i]:
                for o in range(len(anlamlar[i]["orneklerListe"])):
                    sonuc += "_Örnek:_ " + \
                        anlamlar[i]["orneklerListe"][o]["ornek"] + "\n"
                    if "yazar" in anlamlar[i]["orneklerListe"][o]:
                        sonuc += "\t\t_ -" + \
                            anlamlar[i]["orneklerListe"][o]["yazar"][0]["tam_adi"] + "_\n\n"
                    else:
                        sonuc += "\n"
            else:
                sonuc += "\n"

        print("\t*** DISCORD BOT ***\n")
        await message.reply(sonuc, mention_author=False)


client = tdksozluk()
client.run(token_discord)


### DISCORD BOT ###
