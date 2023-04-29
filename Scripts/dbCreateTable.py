from constants import dbCreateTable_py
from logger import logger
from sqlite3 import Error
from dbConnect import dbConnect


def dbCreateTable(sqlQuery):
    conn = dbConnect(dbCreateTable_py)
    try:
        c = conn.cursor()
        c.execute(sqlQuery)
        logger(dbCreateTable_py, f'Success : Initialised database.')
        return True
    except Error as e:
        logger(dbCreateTable_py, f'Error   : {e}')
        return False


def dbCreateTables():
    createTable_IndexData_sql = ''' CREATE TABLE IF NOT EXISTS "IndexData" (
                                    "object_id"	VARCHAR(31) NOT NULL,
                                    "host"	VARCHAR(255) NOT NULL,
                                    "work_id"	VARCHAR(255) NOT NULL,
                                    "url"	VARCHAR(255) NOT NULL,
                                    "metadata" INT NOT NULL DEFAULT 0,
                                    "unavailable"	INT NOT NULL DEFAULT 0,
                                    "favourite"	INT NOT NULL DEFAULT 0,
                                    "saved" INT NOT NULL DEFAULT 0,
                                    "entry_date" DATETIME DEFAULT (datetime('now','localtime')),
                                    "user_tags" TEXT,	
                                    "title" TEXT,	
                                    "series" TEXT,
                                    "authors" TEXT,
                                    "summary" TEXT,
                                    "fandoms" TEXT,
                                    "tags" TEXT,
                                    "characters" TEXT,
                                    "categories" TEXT,
                                    "relationships" TEXT,
                                    "warnings" TEXT,
                                    "status" TEXT,
                                    "rating" TEXT,
                                    "language" TEXT,
                                    "chapters" INT,
                                    "words" INT,
                                    "hits" INT,
                                    "kudos" INT,
                                    "date_edited" DATETIME,
                                    "date_published" DATETIME,
                                    "date_updated" DATETIME,
                                    PRIMARY KEY("object_id")
                                );'''

    createTable_AO3Login_sql = ''' CREATE TABLE IF NOT EXISTS "AO3Login" (
                                    "username"	VARCHAR(255) NOT NULL,
                                    "password"	VARCHAR(255) NOT NULL,
                                    "selected" INT NOT NULL DEFAULT 0,
                                    PRIMARY KEY("username")
                                );'''

    dbCreateTable(createTable_IndexData_sql)
    dbCreateTable(createTable_AO3Login_sql)


if __name__ == '__main__':
    dbCreateTable()
