from constants import getObjectIDfromURL_py
from logger import logger


def getObjectIDfromURL(URL):
    try:
        URL_Split_1 = URL.split('/')
        URL_Split_2 = URL_Split_1[0].split('?')
        URL_Split_3 = URL_Split_2[0].split('-')
        URL_Split_4 = URL_Split_3[0].split('#')
        ObjectID = str(URL_Split_4[0])
        return ObjectID
    except Exception as e:
        logger(getObjectIDfromURL_py, f'Error   : {e}')
        return None


if __name__ == '__main__':
    link = 'https://www.tthfanfic.org/Story-8763-8/WhiteWolf+Willow+meets+Harry+and+Dementors.htm#storybody'
    print(getObjectIDfromURL(link.split(r'tthfanfic.org/Story-')[1]))



