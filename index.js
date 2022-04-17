/* index.js */

const request = require("request");
const https = require('https');

const TelegramBot = require('node-telegram-bot-api');

// replace the value below with the Telegram token you receive from @BotFather
const token = process.env.TDKSOZLUKBOT_TOKEN;

https.createServer(function (req, res) {
    res.writeHead(200);
    res.end("<html><title>tdk telegram bot by berkantkz</title><meta http-equiv='refresh' content='5; url=http://sozluk.gov.tr/'/><body><a href='https://t.me/berkantkz'>berkantkz</a></body></html>");
  }).listen(process.env.PORT || 5000);

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, { polling: true });

bot.on("inline_query", function (q) {
    let query = encodeURIComponent(q.query.trim())
    var veri = q;
    var terim = veri.query.toLowerCase();
    var kimlik = veri.id;
    var lisan = "";
    var anlamlar = "";
    console.log(q);

    request.get({
        url: encodeURI("https://sozluk.gov.tr/gts?ara=" + terim),
        json: true,
        headers: { 'User-Agent': 'request' },
    }, (err, res, data) => {
        if (err) {
            console.log('Error:', err);
        } else if (res.statusCode !== 200) {
            console.log('Status:', res.statusCode);
        } else {
            if (data[0] == undefined) return console.log("sonuç yok");
            console.log(data[0]);

            lisan = String(data[0].lisan) != "" ? data[0].lisan : "Türkçe";

            for (i = 0; i < data[0].anlamlarListe.length; i++) {
                anlamlar += (i + 1) + ": " + String(data[0].anlamlarListe[i].anlam) + "\n\n";
            };

            bot.answerInlineQuery(kimlik, [{
                "id": query,
                "type": "article",
                "title": String(terim),
                "description": String(anlamlar.split("\n")[0].replace(/\*/g, '')),
                "input_message_content": {
                    "message_text": terim + ":\n\n" + String(anlamlar) + "\nDil: " + lisan,
                    "parse_mode": "html"
                }
            }]);
        }
    });
});

bot.onText('/yardim', (msg, match) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "Bu bot sohbet içinde anlık olarak @tdksozlukbot [sözcük] komutu ile sozluk.gov.tr adresinde yer alan Türkçe sözcüklerin anlamını çekmek için oluşturulmuştur. \n\n Bu ekranda arama yapmak için aynı komut kullanılabilir.\n\nHiçbir şekilde Türk Dil Kurumu ile bağlantısı bulunmamaktadır.\n\nhttps://github.com/berkantkz/telegram-inline-turkce-sozluk-nodejs")
});

bot.onText('/help', (msg, match) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "This bot was created to fetch the Turkish meanings placed at sozluk.gov.tr via @tdksozlukbot [word] command instantly right on chat screen.\n\n The same command can be used when chatting with bot as well.\n\nNot affiliated with Turkish Language Society in any way.\n\nhttps://github.com/berkantkz/telegram-inline-turkce-sozluk-nodejs")
});