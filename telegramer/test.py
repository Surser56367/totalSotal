import random
import sqlite3
import datetime

con = sqlite3.connect("test.db")
cur = con.cursor()


def create():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       gameId PRIMARY KEY,
       userid TEXT,
       numer TEXT,
       data TEXT,
       infoId TEXT);
    """)
    con.commit()


def addInfo():
    user = ("99", "99", "99", "2022-07-14", "gr")
    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", user)
    con.commit()


def delete():
    cur.execute("DELETE FROM users WHERE gameId='2';")
    con.commit()


def getInfo():
    cur.execute("SELECT * FROM users;")
    all_results = cur.fetchall()
    return all_results


def getUserInName():
    cur.execute("select * from users where gameId='0'")
    print(cur.fetchall())
    fe = "2022-07-12"

    dat = datetime.date.today()
    if str(dat) != fe:
        print("+")
    else:
        print("wait")
    print(dat)

    sist = ('1', '1', '1', 'testBot')
    for i in sist:
        print(i)


def edit():
    cur.execute(f'UPDATE users SET data = ? WHERE gameId = ?', (f"{da}", f"{1}"))
    con.commit()
    #    cur.execute(f'UPDATE users SET data = ? WHERE gameId = ?', ("2022-07-17", "0"))
    cur.execute(f'UPDATE users SET numer = ? WHERE gameId = ?', (f"{random.randint(0, 12)}", f"0"))
    con.commit()


def g():
    """cur.execute("select * from users where gameId='{}'".format(0))
    userInfo = cur.fetchall()
    print(userInfo[0][3])
    """


def get():
    cur.execute(" SELECT numer, userId FROM users")
    all_results = cur.fetchall()
    print(all_results)
    leaders = []
    message = "Первое место: {}\nВторое место: {}\nТретье место: {}\nЧетрвёртое место: {}\nПятое место: {}"
    for top5 in all_results:
        leaders.append(top5[1])

    print(message.format(leaders[0], leaders[1], leaders[2], leaders[3], leaders[4]))


def new():
    cur.execute("""CREATE TABLE IF NOT EXISTS c{}(
           gameId PRIMARY KEY,
           userId TEXT,
           numer TEXT,
           warning TEXT,
           personality TEXT,
           donate TEXT,
           sigId TEXT);
        """.format(abs(-1001671239319)))
    con.commit()


user = (f"{0}", f"{0}", "0", "0", "2022-07-14", "0", "None")
cur.execute("INSERT INTO c{} VALUES(?, ?, ?, ?, ?, ?, ?);".format(abs(-1001671239319)), user)
con.commit()




