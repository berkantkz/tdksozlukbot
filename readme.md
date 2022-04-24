[Türkçe](#türkçe)

[English](#english)

---

###### Türkçe

# Discord & Telegram TDK Sözlük bot
> Bu python betiği, aynı anda hem Telegram hem de Discord botu çalıştırır. Ayrı ayrı olarak çalıştırmak mümkün değildir (şimdilik).

Sohbet içerisinde doğrudan olarak sözcük anlamına bakmak için Telegram'da ```@tdksozlukbot [sözcük]``` komutunu girin; Discord'ta ise ```@TDK Sözlük [sözcük]``` mesajını iletin.

# [TDK Sözlük Bot'u Discord sunucunuza ekleyin!](https://discord.com/oauth2/authorize?client_id=966110075901083648&scope=bot&permissions=274878155776)

## Kurulum

> Not: Sisteminizde [python3](https://www.python.org/downloads/) kurulu olmalıdır.

1. Token:
   1. Telegram için: Bot tokeninizi ```TDKSOZLUKBOT_TOKEN``` değişken adıyla environment değişkenlerinize ekleyin ya da ```tdksozlukbot.py``` içerisinde yer alan ```token``` değişkenini botunuzun tokeni ile değiştirin.
   2. Discord için: Bot tokeninizi ```TDKSOZLUKBOT_DISCORD``` değişken adıyla environment değişkenlerinize ekleyin ya da ```tdksozlukbot.py``` içerisinde yer alan ```token_discord``` değişkenini botunuzun tokeni ile değiştirin.

2. Aşağıdaki komutları çalıştırın:
```console
git clone https://github.com/berkantkz/tdksozlukbot
cd tdksozlukbot
pip install -r requirements.txt
python tdksozlukbot.py
```

> Komutları çalıştırırken bot adını oluşturduğunuz botun adı ile değiştirmeyi unutmayın.

## Hata bildirme
[Issues](https://github.com/berkantkz/tdksozlukbot/issues) sekmesi, [telegram hesabı](https://t.me/berkantkz)m ya da berkantkz#7475'ten hataları bildirebilirsiniz.

###### English

# Discord & Telegram TDK Dictionary bot
> This python script launches both Telegram and Discord bot at the same time. It is not possible to run separately (for now).

Use ```@tdksozlukbot [word]``` command on Telegram and send ```@TDK Sözlük [word]``` message on Discord so as to check the meaning of a word right in the chat.

# [Add TDK Sözlük Bot to your Discord server!](https://discord.com/oauth2/authorize?client_id=966110075901083648&scope=bot&permissions=274878155776)

## Installation

> Note: [python3](https://www.python.org/downloads/) must be installed on your system.

1. Tokens
   1. Either add your bot's token as ```TDKSOZLUKBOT_TOKEN``` to your environment variables or change the ```token``` variable inside of ```tdksozlukbot.py``` with your bot's token for Telegram.
   2. Either add your bot's token as ```TDKSOZLUKBOT_DISCORD``` to your environment variables or change the ```token_discord``` variable inside of ```tdksozlukbot.py``` with your bot's token for Discord.
2. Run the commands below:
```console
git clone https://github.com/berkantkz/tdksozlukbot
cd tdksozlukbot
pip install -r requirements.txt
python tdksozlukbot.py
```

> Do not forget to replace the name of the bot with the one you created while using.

## Reporting issues
Issues can be reported via [Issues](https://github.com/berkantkz/tdksozlukbot/issues) tab or my [telegram account](https://t.me/berkantkz) or berkantkz#7475.
