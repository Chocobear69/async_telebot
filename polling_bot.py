import aiohttp
import asyncio
import datetime


telegram_api_url = "https://api.telegram.org/bot883751338:AAEFIPpzP4F-awZDO6-8K9uHhq97XlXWx5U/{method}"


async def send_message(chat_id, session):
    now = datetime.datetime.now()
    data = {"chat_id": chat_id, "text": "TODAY IS: " + str(now.ctime())}
    async with session.post(telegram_api_url.format(method="sendMessage"), data=data) as response:
        pass


async def get_update():
    update_number = None
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(telegram_api_url.format(method="getUpdates")) as response:
                r = await response.json()
                if (new_update_number := r["result"][-1]["update_id"]) != update_number:
                    print(new_update_number)
                    update_number = new_update_number
                    await send_message(r["result"][-1]["message"]["chat"]["id"], session)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(get_update())
    loop.run_forever()
