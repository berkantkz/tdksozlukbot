# TDK Sözlük bot
#
# berkantkz

# GLOBALS

import re
import discord
from telegram.utils.helpers import escape_markdown
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, ChosenInlineResultHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, InlineKeyboardMarkup, InlineKeyboardButton
import tdk.gts
import tdk.tools
import tdk.models
from tdk.exceptions import TdkSearchErrorException
from uuid import uuid4
import logging
import os
from dotenv import load_dotenv
from hashlib import md5

### TELEGRAM BOT ###

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TDK_INDEX = tdk.gts.index()
HASH_LUT = {md5(word.encode("utf-8"), usedforsecurity=False).hexdigest(): word for word in TDK_INDEX}
SEARCH_IDS_CACHE = {}
ID_DATA_CACHE = {}  # The entire dictionary takes only about 80 MB.

__tdk_gts_search = tdk.gts.search
def __tdk_gts_search__hook(query: str) -> list[tdk.models.Entry]:
    global SEARCH_IDS_CACHE
    global ID_DATA_CACHE

    if query in SEARCH_IDS_CACHE:
        print("Cache hit for "+query)
        return list(map(ID_DATA_CACHE.get, SEARCH_IDS_CACHE[query]))

    print("Cache miss on "+query)
    try:
        entries = __tdk_gts_search(query)
    except TdkSearchErrorException:
        SEARCH_IDS_CACHE[query] = []
        return []
    SEARCH_IDS_CACHE[query] = list(map(lambda entry: entry.tdk_id, entries))
    for entry in entries:
        ID_DATA_CACHE[entry.tdk_id] = entry

    return __tdk_gts_search__hook(query)
tdk.gts.search = __tdk_gts_search__hook

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

    prompt_entries = filter(lambda s: s.startswith(query), TDK_INDEX)
    if not prompt_entries:
        update.inline_query.answer([])
        return

    update.inline_query.answer([
        InlineQueryResultArticle(
            id=md5(word.encode("utf-8"), usedforsecurity=False).hexdigest(),
            title=word,
            input_message_content=InputTextMessageContent(
                f"Sözcük bilgisi alınıyor: {word}",
                parse_mode=ParseMode.MARKDOWN
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Sözcük yükleniyor...", callback_data="1")
            ]])
        ) for word in prompt_entries
    ], auto_pagination=True)

def queryresult_chosen(update: Update, context: CallbackContext) -> None:
    word_hash = update.chosen_inline_result.result_id
    inline_message_id = update.chosen_inline_result.inline_message_id
    context.bot.edit_message_text(
        inline_message_id=inline_message_id,
        text=prepare_text_from_word(tdk.gts.search(HASH_LUT[word_hash])[0], platform="telegram"),
        parse_mode=ParseMode.MARKDOWN
    )

def run_telegram_bot() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(telegram_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    dispatcher.add_handler(ChosenInlineResultHandler(queryresult_chosen))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


### TELEGRAM BOT ###

### DISCORD BOT ###

class tdksozluk(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if not (client.user.mentioned_in(message)) or "@everyone" in message.content:
            return

        print("\n\t*** DISCORD BOT ***")

        if message.author != client.user:
            print('Message from {0.author}: {0.content}'.format(message))

        query = re.sub("<@\d{18}> +", "",
                       re.sub(" +", " ",  message.content))

        arama_sonuclari = tdk.gts.search(query)
        if not arama_sonuclari:
            return await message.reply("**Aranan söz Türk Dil Kurumu'nun Güncel Türkçe Sözlük'ünde mevcut değil.**", mention_author=False)

        metin = prepare_text_from_word(arama_sonuclari[0], platform="discord")

        print("\t*** DISCORD BOT ***\n")
        if len(metin) > 2000:
            await message.reply(embed=discord.Embed(title="", description=metin), mention_author=False)
        else:
            await message.reply(metin, mention_author=False)

### DISCORD BOT ###


formatters = {
    "discord": {
        "bold": lambda t: f"**{t}**",
        "italic": lambda t: f"*{t}*",
    },
    "telegram": {
        "bold": lambda t: f"**{t}**",
        "italic": lambda t: f"__{t}__",
    },
}


def prepare_text_from_word(word: tdk.models.Entry, platform: str):
    """Verilen tdk-py Entry'sinden mesaj olarak gönderilebilen, Markdown formatında bir metin hazırlar."""
    
    bold = formatters[platform]["bold"]
    italic = formatters[platform]["italic"]

    metin = ""

    if word.prefix:
        metin += bold("(" + word.prefix + "-)") + " "
    metin += bold(word.entry)
    if word.order > 0:
        metin += bold("(" + word.order + ")") + " "
    metin += "\n"
    if word.suffix:
        metin += italic("(-"+ word.suffix + ")") + "\n"
    if word.original:
        metin += italic("(" + word.original + ")") + "\n"
    if word.pronunciation:
        metin += italic("(" + word.pronunciation + ")") + "\n"
    if word.plural:
        metin += italic("(çoğul)") + "\n"
    if word.proper:
        metin += italic("(özel)") + "\n"

    metin += "\n" + bold("Anlamlar:") + "\n"
    for number, meaning in enumerate(word.meanings, start=1):
        metin += f"\n{number}. "
        for meaning_property in meaning.properties:
            metin += italic("(" + meaning_property.value.full_name + ")") + " "
        metin += meaning.meaning + "\n"
        if meaning.examples:
            metin += "\n    " + bold("Örnek kullanımlar:") + "\n"
            for example_number, example in enumerate(meaning.examples, start=1):
                metin += f"    {example_number}. {example.example}\n"
                if example.writer:
                    metin += "        "+bold(example.writer.full_name) + "\n"

    if word.proverbs:
        metin += "\n"+ bold("Atasözleri, deyimler ve birleşik sözcükler:") + "\n"
    for number, proverb in enumerate(word.proverbs, start=1):
        metin += f"{number}. {proverb.proverb}\n"

    metin += "\n" + bold("Heceler:") + "\n" + '/'.join(tdk.tools.hecele(word.entry))
    return metin

if __name__ == '__main__':
    telegram_token = os.getenv("TELEGRAM_TOKEN") or os.getenv("TDKSOZLUKBOT_TOKEN")
    discord_token = os.getenv("DISCORD_TOKEN") or os.getenv("TDKSOZLUKBOT_DISCORD")

    client = tdksozluk()
    client.run(discord_token)

    run_telegram_bot()
