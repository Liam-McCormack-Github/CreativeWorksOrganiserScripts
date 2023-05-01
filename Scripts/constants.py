from os.path import abspath, dirname, join

# Text Constants
https = r'https://www.'
no_ID = r'__ID_NOT_FOUND__'

# Directories
root_dir = dirname(dirname(abspath(__file__)))
py_dir = join(root_dir, 'Scripts')
data_dir = join(root_dir, 'Data')
download_storage_dir = join(root_dir, 'Storage')

temp_dir = join(data_dir, 'Temp')
log_dir = join(data_dir, 'Log')
storage_dir = join(data_dir, 'Storage')
input_dir = join(temp_dir, 'Input')

# Files
log_file = join(log_dir, 'log.txt')
temp_file = join(temp_dir, 'temp.txt')
db_file = join(storage_dir, 'index.db')

# Scripts Names
startup_py = r'startup.py'
dbConnect_py = r'dbConnect.py'
dbCreateTable_py = r'dbCreateTable.py'
getLinksFromInputs_py = r'getLinksFromInputs.py'
insertLinksIntoDB_py = r'insertLinksIntoDB.py'
validateURL_py = r'validateURL.py'
getObjectIDfromURL_py = r'getObjectIDfromURL.py'
getMetadataForDB_py = r'getMetadataForDB.py'
module_ffn_py = r'module_ffn.py'
WorkMetadata_py = r'WorkMetadata.py'
tempPause_py = r'tempPause.py'
electron_downloadWorkFromInternet_py = r'downloadWork.py'
electron_fetchDataFromInternet_py = r'fetchMetadata.py'
getInputs_py = r'getInputs.py'
logger_py = r'logger.py'
checkDir_py = r'checkDir.py'
checkFile_py = r'checkFile.py'
constants_py = r'constants.py'
databaseFunctions_py = r'databaseFunctions.py'

