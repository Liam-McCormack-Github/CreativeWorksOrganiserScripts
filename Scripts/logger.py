# Project Imports
from constants import log_file, logger_py


def logger(caller, content, suppress=False):
    if not suppress:
        try:
            with open(log_file, "a", encoding='utf-8') as logFile:
                logFile.write(f'{caller:<21} : {content}\n')
                logFile.close()
        except FileNotFoundError as e:
            print(f'logger {e}')


if __name__ == '__main__':
    logger(logger_py, 'testing logger')




