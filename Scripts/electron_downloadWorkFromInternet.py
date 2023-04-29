from sys import argv, stdout
from module_ao3 import host_ao3
from module_tth import host_tth
from classWorkMetadata import WorkMetadata
from logger import logger
from constants import electron_downloadWorkFromInternet_py


def electron_downloadWorkFromInternet():
    argv.pop(0)
    downloadFormat = argv[0]
    argv.pop(0)
    logger(electron_downloadWorkFromInternet_py, f'Attempting to download {len(argv)} Works as {downloadFormat}')
    for count, objectID in enumerate(argv, start=1):
        work = WorkMetadata({'object_id': objectID})
        if work.host == host_ao3:
            work.downloadWorkViaModules(downloadFormat)
        if work.host == host_tth:
            work.downloadWorkViaModules(downloadFormat)
        logger(electron_downloadWorkFromInternet_py, f'{count}/{len(argv)} : {objectID}')
    stdout.flush()


if __name__ == '__main__':
    electron_downloadWorkFromInternet()
