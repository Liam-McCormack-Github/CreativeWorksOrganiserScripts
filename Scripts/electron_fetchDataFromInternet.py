from sys import argv, stdout
from module_ao3 import host_ao3
from module_tth import host_tth
from module_ffn import host_ffn
from classWorkMetadata import WorkMetadata
from logger import logger
from constants import electron_fetchDataFromInternet_py


def electron_fetchDataFromInternet():
    argv.pop(0)
    logger(electron_fetchDataFromInternet_py, f'Attempting to retrieve meta data for {len(argv)} Works')
    for count, objectID in enumerate(argv, start=1):
        work = WorkMetadata({'object_id': objectID})
        if work.host == host_ao3:
            work.getMetadataViaModules()
        if work.host == host_tth:
            work.getMetadataViaModules()
        if work.host == host_ffn:
            work.getMetadataViaModules()
        logger(electron_fetchDataFromInternet_py, f'{count}/{len(argv)} : {objectID}')
    stdout.flush()


if __name__ == '__main__':
    electron_fetchDataFromInternet()
