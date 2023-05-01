import AO3
import sqlite3

from sqlite3 import Error
from re import sub
from os.path import isfile, join

from dbConnect import dbConnect
from logger import logger
from tempPause import tempPause
from constants import download_storage_dir

# Module Constants
host_ao3 = r'AO3'
url_indicates_ao3 = r'archiveofourown.org/works/',
module_ao3_py = r'module_ao3.py'
valid_download_formats_ao3 = ('HTML', 'EPUB', 'MOBI', 'AZW3', 'PDF')


def getLoginForAO3():
    conn = dbConnect(module_ao3_py, True)
    c = conn.cursor()
    c.execute(f'''SELECT "username", "password" FROM AO3Login WHERE selected=1;''')
    rows = c.fetchall()
    if rows:
        ao3_username = rows[0][0]
        ao3_password = rows[0][1]
        return True, ao3_username, ao3_password
    else:
        logger(module_ao3_py, f'Error   : Credentials Not found in Database.')
        return False, '', ''




def findWorkThroughAPI(workID):
    loop_stage = 1
    '''
    Loop Stage 1 = Initial Stage, trying to find work
    Loop Stage 2 = Work Need login to be found, login and try again
    Loop Stage 3 = Work Could Not be Found, break loop
    Loop Stage 4 = Work Found, break loop
    '''
    while loop_stage != 4:
        if loop_stage == 3:
            logger(module_ao3_py, f'Could Not Find Work {workID}')
            return None
        elif loop_stage == 1:
            try:
                work = AO3.Work(workID)
                logger(module_ao3_py, f'Success : Found info for AO3_{workID}')
                return work
            except AO3.utils.InvalidIdError:
                loop_stage = 2
                logger(module_ao3_py, f'Warning : Invalid Id AO3_{workID} --Attempt to try with credentials')
            except AO3.utils.HTTPError:
                tempPause()
                loop_stage = 1
                logger(module_ao3_py, f'Warning : HTTPError AO3_{workID} --Pausing to reset time out')
            except AttributeError:
                loop_stage = 2
                logger(module_ao3_py, f'Warning : AttributeError AO3_{workID} --Attempt to try with credentials')
            except Exception as e:
                loop_stage = 3
                logger(module_ao3_py, f'Error   : {e} AO3_{workID}')
        elif loop_stage == 2:
            try:
                credentialsFound, ao3_username, ao3_password = getLoginForAO3()
                if credentialsFound:
                    session = AO3.Session(ao3_username, ao3_password)
                    work = AO3.Work(workID, session)
                    logger(module_ao3_py, f'Success : Found info for AO3_{workID} --Needed to login')
                    return work
                else:
                    loop_stage = 3
                    logger(module_ao3_py, f'Error   : Credentials not found. Please register your login credentials in the Settings page.')

            except AO3.utils.InvalidIdError:
                loop_stage = 3
                logger(module_ao3_py, f'Error   : Invalid Id AO3_{workID} --Tried with credentials')
            except AO3.utils.HTTPError:
                tempPause()
                loop_stage = 2
                logger(module_ao3_py, f'Warning : HTTPError AO3_{workID} --Trying again after 5 Minutes, with credentials')
            except AttributeError:
                loop_stage = 3
                logger(module_ao3_py, f'Error   : AttributeError AO3_{workID}')
            except Exception as e:
                loop_stage = 3
                logger(module_ao3_py, f'Error   : {e} AO3_{workID}')


def downloadWorkFromID_ao3(workID, title, downloadFormat):
    if downloadFormat not in valid_download_formats_ao3:
        logger(module_ao3_py, f'Error   : Selected Format for download of AO3_{workID} is {downloadFormat} which is not supported. Changing format to {valid_download_formats_ao3[0]}')
        downloadFormat = valid_download_formats_ao3[0]

    work = findWorkThroughAPI(workID)

    if not work:
        return False

    title = title if title != '' else work.title
    cleanTitle = sub(r'[^\w\.\-]', ' ', title)
    fileName = f'AO3_{workID}_{cleanTitle}'
    filePath = join(download_storage_dir, f'{fileName}.{downloadFormat}')
    with open(filePath, 'wb') as file:
        file.write(work.download(downloadFormat))
        file.close()

    if isfile(filePath):
        return True


def fetchMetadataFromID_ao3(workID):
    work = findWorkThroughAPI(workID)

    if not work:
        return {'unavailable': '1'}

    workMetadata = work.metadata
    work_title = workMetadata['title']
    work_summary = workMetadata['summary']
    work_summary = work_summary.strip()
    work_summary = sub('\n', ' ', work_summary)
    work_summary = sub(' {2}', ' ', work_summary)
    work_summary = work_summary.encode('utf-8', 'ignore').decode('utf-8')
    work_series = tuple(workMetadata['series'])
    work_authors = tuple(workMetadata['authors'])
    work_fandoms = tuple(workMetadata['fandoms'])
    work_tags = tuple(workMetadata['tags'])
    work_characters = tuple(workMetadata['characters'])
    work_categories = tuple(workMetadata['categories'])
    work_relationships = tuple(workMetadata['relationships'])
    work_warnings = tuple(workMetadata['warnings'])
    work_status = workMetadata['status']
    work_rating = workMetadata['rating']
    work_language = workMetadata['language']
    work_chapters = workMetadata['nchapters']
    work_words = workMetadata['words']
    work_hits = workMetadata['hits']
    work_kudos = workMetadata['kudos']
    work_date_edited = workMetadata['date_edited']
    work_date_published = workMetadata['date_published']
    work_date_updated = workMetadata['date_updated']

    data = {'metadata': 1,
            'title': work_title,
            'summary': work_summary,
            'series': work_series,
            'authors': work_authors,
            'fandoms': work_fandoms,
            'tags': work_tags,
            'characters': work_characters,
            'categories': work_categories,
            'relationships': work_relationships,
            'warnings': work_warnings,
            'status': work_status,
            'rating': work_rating,
            'language': work_language,
            'chapters': work_chapters,
            'words': work_words,
            'hits': work_hits,
            'kudos': work_kudos,
            'date_edited': work_date_edited,
            'date_published': work_date_published,
            'date_updated': work_date_updated}
    return data


def module_ao3():
    pass


if __name__ == '__main__':
    # ao3_insert_metaData(43715991)
    # module_ao3()
    # print(fetchMetadataFromID_ao3(46165906))
    print(getLoginForAO3())
    # test = downloadWorkFromID_ao3(46165906, '', 'pdf')
    # print(test)
    # print(fetchMetadataFromID_ao3(27946634))
    # print(fetchMetadataFromID_ao3(28475718))
