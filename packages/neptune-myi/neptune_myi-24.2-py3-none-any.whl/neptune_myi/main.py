import qrcode
import sqlite3
from termcolor import colored
from colorama import init

init()

def qrmake(qrname, qrsave):
    qr = qrcode.make(qrname)
    qr.save(qrsave)

def sql(connection, command):
    db = sqlite3.connect(connection)
    sql = db.cursor()

    sql.execute(command)
    db.commit()

qizil = "red"
yashil = "green"
kok = "blue"
och_kok = "cyan"
pushti = "magenta"

def rangli(rang, tekst):

    print(colored(tekst, rang))

    