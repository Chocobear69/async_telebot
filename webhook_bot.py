import logging
import ssl

from aiohttp import web
import telebot

from config import (
    API_TOKEN,
    WEBHOOK_PORT,
    WEBHOOK_LISTEN,
    WEBHOOK_SSL_CERT,
    WEBHOOK_SSL_PRIV,
    WEBHOOK_URL_BASE,
    WEBHOOK_URL_PATH
)


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)


class Handler(web.View):
    async def post(self):
        if self.request.match_info.get('token') == bot.token:
            request_body_dict = await self.request.json()
            update = telebot.types.Update.de_json(request_body_dict)
            bot.process_new_updates([update])
            return web.Response()
        else:
            return web.Response(status=403)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "What is up, Nigger!")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    app = web.Application()
    app.router.add_view('/{token}/', Handler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))

    web.run_app(
        app,
        host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=context,
    )
