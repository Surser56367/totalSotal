import asyncio
import datetime
import random
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
import botButton
import sqlite3

token = "5380908893:AAHdaqdrPDdacx8x-0WtDR0Ul9BGXebBXv8"
primer = []
bot = Bot(token=token)
dp = Dispatcher(bot=bot)
Command = aiogram.dispatcher.filters.Command


@dp.message_handler(Command(commands="user", prefixes="!"))
async def get_info_user(msg: types.Message):
    user = types.User.get_current()
    await msg.answer(msg.from_user.id)


@dp.message_handler(Command(commands="admins", prefixes="!"))
async def admins_panels(msg: types.Message):
    chat_admins = await bot.get_chat_administrators(msg.chat.id)
    for admins in chat_admins:
        userId = admins.user.id
        if msg.from_user.id == userId:
            await msg.answer("Админ панель выведена вам на экран!", reply_markup=botButton.KeyButton().adminsRoot())


@dp.message_handler(Command(commands="game", prefixes="!"))
async def game_model(msg: types.Message):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    userId = types.User.get_current().id
    cur.execute("""CREATE TABLE IF NOT EXISTS c{}(
                       gameId PRIMARY KEY,
                       userId TEXT,
                       numer TEXT,
                       warning TEXT,
                       personality TEXT,
                       donate TEXT,
                       sigId TEXT);
                    """.format(abs(msg.chat.id)))
    con.commit()
    cur.execute("select * from c{} where userId='{}'".format(abs(msg.chat.id), str(userId)))
    con.commit()
    userInfo = cur.fetchall()
    if userInfo == []:
        cur.execute("SELECT * FROM c{};".format(abs(msg.chat.id)))
        f = cur.fetchmany(-1)
        try:
            i = f[-1][0]
        except IndexError:
            i = "0"
        num = int(i[0]) + 1
        user = (f"{num}", f"{userId}", "0", "0", "2022-07-14", "0", "None")
        cur.execute(f"INSERT INTO c{abs(msg.chat.id)} VALUES(?, ?, ?, ?, ?, ?, ?);", user)
        con.commit()

        await msg.reply(
            "Добро пожаловать в игру, @{}! у вас {} очков! Ваш id в боте: {}. Донат валюта: 0".format(
                types.User.get_current().username, 0, num))
    else:
        await msg.answer("Вы уже прошли регистрацию!\nДля получения ежедневного приза используйте команду !check")


@dp.message_handler(Command(prefixes="!", commands="check"))
async def main_game(msg: Message):
    try:
        con = sqlite3.connect("test.db")
        cur = con.cursor()
        cur.execute("select * from c{} where userId='{}'".format(abs(msg.chat.id), str(types.User.get_current().id)))
        userInfo = cur.fetchall()
        gameId = userInfo[0][0]
        dateCh = userInfo[0][4]
        newDate = datetime.date.today()
        newNumer = userInfo[0][2]
        BonusPoints = random.randint(1, 12)
        if str(newDate) == str(dateCh):
            await msg.answer("Вы уже отметились сегодня!")
        else:
            cur.execute(f'UPDATE c{abs(msg.chat.id)} SET personality = ? WHERE gameId = ?', (f"{newDate}", f"{gameId}"))
            con.commit()
            cur.execute(f'UPDATE c{abs(msg.chat.id)} SET numer = ? WHERE gameId = ?',
                        (f"{int(newNumer) + BonusPoints}", f"{gameId}"))
            con.commit()
            await msg.answer("Вы получили: {} очков! Жду завтра.".format(BonusPoints))
    except:
        await msg.answer("Вы еще не зарегистрированы")


@dp.message_handler(Command(prefixes="!", commands="монетка"))
async def random_roll(msg: Message):
    await msg.answer("Выпало: {}".format(random.choice(["Oрёл", "Решка"])))


@dp.message_handler(Command(prefixes="!", commands="top"))
async def game_get_top_users(msg: Message):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    cur.execute(f"SELECT numer, userId FROM c{abs(msg.chat.id)}")
    all_results = cur.fetchall()
    leaders = []
    message = "Первое место: {}\nВторое место: {}\nТретье место: {}\nЧетрвёртое место: {}\nПятое место: {}"
    for top5 in all_results:
        leaders.append(top5[1])
    try:
        await msg.answer(message.format(leaders[0], leaders[1], leaders[2], leaders[3], leaders[4]))
    except:
        await msg.answer("В чате мало участников")


@dp.message_handler(Command(prefixes="!", commands="donate"))
async def premium_users(msg: Message):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    cur.execute("select * from c{} where userId='{}'".format(abs(msg.chat.id), str(types.User.get_current().id)))
    userinfo = cur.fetchall()
    donate = userinfo[0][5]
    if int(donate) == 0:
        await msg.reply(f"У вас 0 донат кристалов!\nСкорее преобрети их!\n\nКупить можно тут: @kvorder")
    else:
        await msg.reply("Ваш баланс: {}".format(donate))


@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS, types.ContentType.LEFT_CHAT_MEMBER])
async def new_users(msg: Message):
    if msg["new_chat_members"]:
        await bot.send_message(msg.chat.id, "{}, добро пожаловать в чат!".format(
            f"{msg.from_user.first_name} {msg.from_user.last_name}"))
    else:
        await bot.send_message(msg.chat.id, "Наконец-то он вышел..")


@dp.message_handler(Command(prefixes="!", commands="test"))
async def test(msg: Message):
    await msg.answer(parse_mode=types.ParseMode.HTML, text='<a href="https://google.com">Google</a>')
    await msg.answer(parse_mode=types.ParseMode.HTML, text='<a href="https://youtube.com">YouTube</a>')


@dp.callback_query_handler()
async def callback_center(call: types.CallbackQuery):
    if call.data == "adminButton":
        await call.answer("А ты зачем нажал? Ты не админ :-)")


"""@dp.message_handler(content_types=['text'])
async def delete_messages(msg: types.Message):
    for entity in msg.entities:
        if entity.url in [""]:
            await msg.delete()
            await msg.answer("LOH pishet")
            await asyncio.sleep(2)
            await msg.delete()"""

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
