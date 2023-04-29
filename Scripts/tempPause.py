import time
from datetime import datetime, timedelta
from logger import logger
from constants import tempPause_py
import random


def tempPause():
    randomNumber = random.randint(301, 310)
    now = datetime.now()
    result = now + timedelta(seconds=randomNumber)
    logger(tempPause_py, f'Current time is {now:%H:%M:%S}')
    logger(tempPause_py, f'Sleeping for {randomNumber} Seconds')
    logger(tempPause_py, f'Will resume at {result:%H:%M:%S}')

    time.sleep(randomNumber)


if __name__ == '__main__':
    tempPause()



