from classWorkMetadata import WorkMetadata
from dbConnect import dbConnect
from module_ao3 import host_ao3
from module_tth import host_tth
from logger import logger
from constants import getMetadataForDB_py


def getMetadataForDB():
    conn = dbConnect()
    c = conn.cursor()
    c.execute('''SELECT object_id FROM IndexData WHERE metadata=0 and unavailable != 1;''')
    rows = c.fetchall()
    num_of_works = len(rows)

    if num_of_works == 0:
        logger(getMetadataForDB_py, f'Error   : SQL Query did not return any rows')
        return

    logger(getMetadataForDB_py, f'Success : SQL Query returned {num_of_works} Rows')

    for count, objectID in enumerate(rows, start=0):
        work = WorkMetadata({'object_id': objectID[0]})
        if work.host == host_ao3:
            work.getMetadataViaModules()
        if work.host == host_tth:
            work.getMetadataViaModules()


if __name__ == '__main__':
    getMetadataForDB()
