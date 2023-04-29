from constants import temp_file, insertLinksIntoDB_py
from logger import logger
from getObjectIDfromURL import getObjectIDfromURL
from module_tth import url_indicates_tth, host_tth
from module_ao3 import url_indicates_ao3, host_ao3
from module_ffn import url_indicates_ffn, host_ffn
from classWorkMetadata import WorkMetadata


def insertLinksIntoDB():
    try:
        with open(temp_file, 'r') as f:
            fileContent = f.read().split('\n')
            f.close()
    except FileNotFoundError:
        return False

    print(len(fileContent))

    if len(fileContent) < 1:
        return False

    for link in fileContent:
        if url_indicates_ao3[0] in link:
            objectID = f'{host_ao3}_{getObjectIDfromURL(link.split(url_indicates_ao3[0])[1])}'
            WorkMetadata({'object_id': objectID})
            logger(insertLinksIntoDB_py, f'Success : {objectID} Found in Database.')
        elif url_indicates_tth[0] in link:
            objectID = f'{host_tth}_{getObjectIDfromURL(link.split(url_indicates_tth[0])[1])}'
            WorkMetadata({'object_id': objectID})
            logger(insertLinksIntoDB_py, f'Success : {objectID} Found in Database.')
        elif url_indicates_tth[1] in link:
            objectID = f'{host_tth}_{getObjectIDfromURL(link.split(url_indicates_tth[1])[1])}'
            WorkMetadata({'object_id': objectID})
            logger(insertLinksIntoDB_py, f'Success : {objectID} Found in Database.')
        elif url_indicates_ffn[0] in link:
            objectID = f'{host_ffn}_{getObjectIDfromURL(link.split(url_indicates_ffn[0])[1])}'
            WorkMetadata({'object_id': objectID})
            logger(insertLinksIntoDB_py, f'Success : {objectID} Found in Database.')
        else:
            logger(insertLinksIntoDB_py, f'Invalid : {link} Could not be inserted into Database.')

    return True


if __name__ == '__main__':
    insertLinksIntoDB()




