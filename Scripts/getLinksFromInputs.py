from os import listdir
from os.path import isfile, join
from constants import input_dir, temp_file, getLinksFromInputs_py
from logger import logger
from bs4 import BeautifulSoup
from validateURL import validateURL


def saveURLtoTemp(content=''):
    with open(temp_file, 'a', encoding='utf-8') as tempFile:
        tempFile.write(f'{content}\n')
        tempFile.close()


def getInputsFromBookmarks(file):
    file_path = fr'{input_dir}\{file}'
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    dt = soup.find_all('dt')

    for i in dt:
        n = i.find_next()
        if n.name != 'h3':
            url = n.get('href')
            if validateURL(url):
                saveURLtoTemp(url)

    log = f'Success : {file}'
    return log


def getInputsFromText(file):
    file = fr'{input_dir}\{file}'
    with open(file, 'r') as f:
        content = f.read().split('\n')
        f.close()

    for url in content:
        if validateURL(url):
            saveURLtoTemp(url)

    log = f'Success : {file}'
    return log


def isHTMLaBookmark(file):
    with open(join(input_dir, file), 'r') as f:
        first_line = f.readline().strip('\n')
        if first_line == '<!DOCTYPE NETSCAPE-Bookmark-file-1>':
            return True
        else:
            return False


def getLinksFromInputs():
    list_of_files = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]

    logger(getLinksFromInputs_py, f'Found   : {list_of_files}')

    if not list_of_files:
        logger(getLinksFromInputs_py, 'No inputs')
        return False

    for file in list_of_files:
        if file.split('.')[1] == 'html':
            if isHTMLaBookmark(file):
                log = getInputsFromBookmarks(file)
            else:
                log = f'Error   : {file} file is not a valid Bookmark-file'
        elif file.split('.')[1] == 'txt':
            log = getInputsFromText(file)
        else:
            log = f'Error   : {file} file type is not support for scrapping inputs.'
        logger(getLinksFromInputs_py, log)

    return True


if __name__ == '__main__':
    print(getLinksFromInputs())
