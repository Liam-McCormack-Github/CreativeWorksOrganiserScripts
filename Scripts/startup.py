from shutil import rmtree
from os import remove
from datetime import datetime
# Project Imports
from checkFile import checkFile
from checkDir import checkDir
from logger import logger
from constants import startup_py, data_dir, log_file, log_dir, temp_dir, storage_dir, input_dir, temp_file, db_file
from dbCreateTable import dbCreateTables


def resetLog():
    try:
        remove(log_file)
    except PermissionError:
        logger(startup_py, checkDir(log_dir)[1])
    except FileNotFoundError:
        logger(startup_py, checkDir(log_dir)[1])


def tempDir():
    try:
        rmtree(temp_dir)
    except PermissionError:
        logger(startup_py, checkDir(temp_dir)[1])
    except FileNotFoundError:
        logger(startup_py, checkDir(temp_dir)[1])


def checkFiles():
    logger(startup_py, checkDir(data_dir)[1])
    logger(startup_py, checkDir(temp_dir)[1])
    logger(startup_py, checkFile(temp_file)[1])
    logger(startup_py, checkDir(input_dir)[1])
    logger(startup_py, checkDir(log_dir)[1])
    logger(startup_py, checkFile(log_file)[1])
    logger(startup_py, checkDir(storage_dir)[1])
    logger(startup_py, checkFile(db_file)[1])


def startup(reset_log=False):
    checkDir(data_dir)

    if reset_log:
        resetLog()

    tempDir()

    logger(startup_py, '---------------------')
    logger(startup_py, f'Starting Main @ {datetime.now()}')
    logger(startup_py, '---------------------')
    checkFiles()
    dbCreateTables()


if __name__ == '__main__':
    startup(True)





