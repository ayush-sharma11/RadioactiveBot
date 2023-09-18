from os.path import isfile
from sqlite3 import connect
from apscheduler.triggers import CronTrigger

DB_PATH = "./data/db/database.py"
BUILD_PATH = "./data/db/build.sql"

cxn = connect(DB_PATH, check_same_thread=False)
cur  = cxn.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
    
    return inner

@with_commit
def build():
    if isfile(BUILD_PATH):
        # checks if build.sql is a file
        scriptexecute(BUILD_PATH)


def commit():
    cxn.commit()

def autosave(sched):
    sched.add_job(commit, CronTrigger(second = 0))


def close():
    cxn.close()

def field(command, *values):
    cur.execute(command, tuple(values))
    # we're passing argument as a list and converting it tuple for aesthetic reasons

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]
        # if the row exists, it gets the first element


def record(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchone()


def records(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchall()


def column(command, *values):
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall]


def execute(command, *values):
    cur.execute(command, tuple(values))


def multiexecute(commands, valueset):
    cur.executemany(commands, valueset)


def scriptexecute(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.execute(script.read())