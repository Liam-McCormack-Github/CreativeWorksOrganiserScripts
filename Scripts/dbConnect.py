from constants import dbConnect_py, db_file
from logger import logger
from sqlite3 import Error, connect


def dbConnect(functionCaller=dbConnect_py, log=False):
    connection = None
    try:
        connection = connect(db_file)
        logger(functionCaller, f'Connect : {db_file}', log)
        return connection
    except Error as e:
        logger(functionCaller, f'Error   : {e}', log)
    return connection


if __name__ == '__main__':
    conn = dbConnect(dbConnect_py)


