# TDK Sözlük bot
#
# berkantkz

# GLOBALS

import re
import discord
from telegram.utils.helpers import escape_markdown
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
import tdk.gts
import tdk.tools
import tdk.models
from uuid import uuid4
import logging
import os

def prepare_text_from_word(word: tdk.models.Entry):
    """Verilen tdk-py Entry'sinden mesaj olarak gönderilebilen, Markdown formatında bir metin hazırlar."""
    metin = ""

    if word.prefix:
        metin = f"{metin}_({word.prefix}-)_ "
    metin = f"{metin}__{word.entry}__ "
    if word.order > 0:
        metin = f"{metin}__({word.order})__"
    metin = f"{metin}\n"
    if word.suffix:
        metin = f"{metin}_(-{word.suffix})_\n"
    if word.original:
        metin = f"{metin}_({word.original})_\n"
    if word.pronunciation:
        metin = f"{metin}_({word.pronunciation})_\n"
    if word.plural:
        metin = f"{metin}_(çoğul)_\n"
    if word.proper:
        metin = f"{metin}_(özel)_\n"

    metin = f"{metin}\nAnlamlar:\n"
    for number, meaning in enumerate(word.meanings, start=1):
        metin = f"{metin}\n{number}. "
        for meaning_property in meaning.properties:
            metin = f"{metin}_({meaning_property.value.full_name})_ "
        metin = f"{metin}{meaning.meaning}\n"
        if meaning.examples:
            metin = f"{metin}\n    __Örnek kullanımlar:__\n"
            for example_number, example in enumerate(meaning.examples, start=1):
                metin = f"{metin}    {example_number}. {example.example}\n"
                if example.writer:
                    metin = f"{metin}        _{example.writer.full_name}_\n"

    if word.proverbs:
        metin = f"{metin}\n__Atasözleri, deyimler ve birleşik sözcükler:__\n"
    for number, proverb in enumerate(word.proverbs, start=1):
        metin = f"{metin}{number}. {proverb.proverb}\n"

    metin = f"{metin}\n__Heceler:__\n{'/'.join(tdk.tools.hecele(word.entry))}"
    return metin

def ara(s):
    try:
        sonuc = tdk.gts.search(s)
    except Exception:
        sonuc = None

    return sonuc

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

    arama_sonuclari = ara(query)
    if arama_sonuclari == None:
        metin = f"__ {query} sözcüğü Türk Dil Kurumu'nun Güncel Türkçe Sözlük'ünde mevcut değil.__"
    else:
        metin = prepare_text_from_word(arama_sonuclari[0])

    son = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=query,
            input_message_content=InputTextMessageContent(metin, parse_mode=ParseMode.MARKDOWN))
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

        query = re.sub("<@966110075901083648> +", "",
                       re.sub(" +", " ",  message.content))

        arama_sonuclari = ara(query)
        if arama_sonuclari == None:
            return await message.reply(f"{query} sözcüğü Türk Dil Kurumu'nun Güncel Türkçe Sözlük'ünde mevcut değil.", mention_author=False)

        metin = prepare_text_from_word(arama_sonuclari[0])

        print("\t*** DISCORD BOT ***\n")
        if len(metin) > 2000:
            await message.reply(embed=discord.Embed(title="", description=metin), mention_author=False)
        else:
            await message.reply(metin, mention_author=False)


client = tdksozluk()
client.run(token_discord)


### DISCORD BOT ###


