from constants import validateURL_py
from logger import logger
from re import compile, search


def validateURL(url):
    regex = '^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$'
    # https://www.makeuseof.com/regular-expressions-validate-url
    r = compile(regex)
    if search(r, url):
        logger(validateURL_py, f'Valid   : {url}', True)
        return True
    else:
        logger(validateURL_py, f'Invalid : {url}', False)
        return False


if __name__ == '__main__':
    print(validateURL('https://en.m.wikipedia.org'))
    print(validateURL('htps://en.m.wikipedia.org'))
    print(validateURL('http://en.m.wikipedia.org/wiki/Jubilee'))
    print(validateURL('https://en.m.wikipedia.org/wiki/Jubilee_(biblical)'))




