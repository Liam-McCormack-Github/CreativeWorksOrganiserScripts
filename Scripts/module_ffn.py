import subprocess
import sqlite3

from constants import download_storage_dir, temp_dir, storage_dir
from logger import logger
from os.path import exists
from os import remove
from re import compile, sub

# Module Constants
host_ffn = r'FFN'
url_indicates_ffn = r'fanfiction.net/s/',
module_ffn_py = r'module_ffn.py'


def downloadWorkFromID_ffn(workID, title, downloadFormat):
    command = [
        "fichub_cli",
        "-u",
        f"https://www.fanfiction.net/s/{workID}",
        "--format",
        "html",
        "-o",
        download_storage_dir
    ]

    print(command)

    result = subprocess.call(command)

    print(result)

    input()


def remove_color_codes(text):
    ansi_escape = compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    text_without_color = ansi_escape.sub('', text)
    return text_without_color


def useShellToCreateMetadataDB(workID):
    command = [
        "fichub_cli",
        "metadata",
        "-i",
        f"https://www.fanfiction.net/s/{workID}",
        "-o",
        r"C:\Users\liam\AppData\Roaming\CreativeWorksOrganiser\Application Storage\Data\Storage"
    ]
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup_info.wShowWindow = subprocess.SW_HIDE

    process = subprocess.Popen(command, startupinfo=startup_info, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate(input="Y")

    return_code = process.returncode
    if return_code == 0:
        pathToOutput = output.split('Metadata saved as ')[1].split('\n')[0]
        pathToOutput = remove_color_codes(pathToOutput)
        return pathToOutput

    else:
        logger(module_ffn_py, f'Error: {error}')
        return None


def queryMetadataDB(workID, outputDB):
    if exists(outputDB):
        conn = sqlite3.connect(outputDB)
        c = conn.cursor()
        query_sql = f'''SELECT "id", 
        "fic_id", 
        "fichub_id", 
        "title", 
        "author", 
        "author_id", 
        "author_url", 
        "chapters", 
        "created", 
        "description", 
        "rated", 
        "language", 
        "genre", 
        "characters", 
        "reviews", 
        "favorites", 
        "follows", 
        "status", 
        "words", 
        "fandom", 
        "fic_last_updated", 
        "db_last_updated", 
        "source"
        FROM fichub_metadata WHERE fic_id = {workID}'''
        c.execute(query_sql)
        rows = c.fetchall()
        conn.close()
        try:
            remove(outputDB)
        except OSError as e:
            logger(module_ffn_py, f"Error deleting the file: {e}")

        return rows[0]


def fetchMetadataFromID_ffn(workID):
    outputDB = useShellToCreateMetadataDB(workID)

    if not outputDB:
        return {'unavailable': '1'}

    fetchData = queryMetadataDB(workID, outputDB)

    for i, value in enumerate(fetchData):
        print(i, value)

    work_title = fetchData[3]
    work_summary = fetchData[9]
    if work_summary is not None:
        work_summary = work_summary.replace('<p>', '', 1).replace('</p>', '', 1)
    work_series = None
    work_authors = fetchData[4]
    work_fandoms = fetchData[19]
    if work_fandoms is not None:
        work_fandoms = work_fandoms.replace(' Crossover', '', 1).replace(' + ', '\n', 1)
    work_tags = fetchData[12]
    work_characters = fetchData[13]
    if work_characters is not None:
        work_characters = work_characters.replace('., ', '.\n', 1)
    work_categories = fetchData[12]
    work_relationships = None
    work_warnings = 'Warnings Not Found'
    work_status = fetchData[17]
    work_rating = fetchData[10]
    work_language = fetchData[11]
    work_chapters = fetchData[7]
    work_words = fetchData[18]
    work_hits = fetchData[16]
    work_kudos = fetchData[15]
    work_date_edited = fetchData[20]
    work_date_published = fetchData[8]
    work_date_updated = fetchData[20]

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


def module_ffn():
    pass


if __name__ == '__main__':
    module_ffn()
    test = fetchMetadataFromID_ffn(14212106)
    print(test)
    # www.fanfiction.net/s/13798037
    # fichub_cli -u "https://www.fanfiction.net/s/13798037" --format html -o "C:\Users\liam\OneDrive\Documents\GitHub\CreativeWorksOrganiserScripts\Scripts\new"
    # fichub_cli metadata -i https://archiveofourown.org/works/10916730/chapters/24276864
    # fichub_cli metadata -i "https://www.fanfiction.net/s/13798037" -o "C:\Users\liam\AppData\Roaming\CreativeWorksOrganiser\Application Storage\Data\Storage"
