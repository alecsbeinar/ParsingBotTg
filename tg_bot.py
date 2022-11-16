import asyncio
import datetime
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink
from aiogram.dispatcher.filters import Text
from config import token
from main import check_news_update, get_news_keyword, get_news_keyword2
from bd import reg_user, get_users, del_user


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
users = get_users()

@dp.message_handler(commands="start")
async def start(message: types.Message):
    answer = reg_user(message)
    if answer is not None:
        await message.answer(answer)
    else:
        global users
        users = get_users()

    start_buttons = ["Все новости", "Последние 5 новостей", "Свежие новости", "Поиск по ключевому слову"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Лента новостей", reply_markup=keyboard)

@dp.message_handler(commands="unsubscribe")
async def start(message: types.Message):
    global users
    users = del_user(message)
    await message.answer("Вы отписались от рассылки новостей")

@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items(), key=lambda x: x[1]['article_date_timestamp']):
        news = f"<b>{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}</b>\n" \
               f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)


@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items(), key=lambda x: x[1]['article_date_timestamp'])[-5:]:
        news = f"<b>{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}</b>\n" \
               f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"<b>{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}</b>\n" \
                   f"{hlink(v['article_title'], v['article_url'])}"

            await message.answer(news)
    else:
        await message.answer("Пока нет свежих новостей...")


@dp.message_handler()
async def get_all_news(message: types.Message):
    await message.answer("Введите ключевое слово")
    news = get_news_keyword2(message.text)
    for k, v in news.items():
        ans = f"<b>{k}</b>\n" \
              f"{v}"
        await message.answer(ans)


async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"<b>{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}</b>\n" \
                       f"{hlink(v['article_title'], v['article_url'])}"

                for u in users:
                    await bot.send_message(int(u[0]), news)
        else:
            for u in users:
                await bot.send_message(int(u[0]), "Пока нет свежих новостей", disable_notification=True)

        await asyncio.sleep(60)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(news_every_minute())
    executor.start_polling(dp)
