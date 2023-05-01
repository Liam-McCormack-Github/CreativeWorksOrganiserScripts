from datetime import datetime

import pytesseract
import requests
from pytesseract import image_to_string, TesseractNotFoundError
from PIL import Image, ImageDraw
from io import BytesIO
from bs4 import BeautifulSoup
from os.path import isfile, join
from re import sub

from constants import download_storage_dir
from logger import logger

# Module Constants
host_tth = r'TTH'
url_indicates_tth = r'tthfanfic.org/Story-', r'tthfanfic.org/wholestory.php?no='
url_tth_story_info = r'https://www.tthfanfic.org/StoryInfo-'
module_tth_py = r'module_tth.py'
valid_download_formats_tth = ('HTML', 'EPUB', 'MOBI', 'TEXT')


def getPointForCrop1(img):
    w = img.width
    h = img.height
    for x in range(w):
        for y in range(h):
            p = img.getpixel((x, y))
            if p == (0, 0, 0):
                return x, y


def getPointForCrop2(img):
    w = img.width
    h = img.height
    for x in range(w):
        for y in range(h):
            p = img.getpixel((w - x - 1, h - y - 1))
            if p == (0, 0, 0):
                return w - x - 1, h - y - 1


def remove_colour_boxes(img):
    w = img.width
    h = img.height
    for x in range(w):
        for y in range(h):
            p = img.getpixel((x, y))
            if p not in (235, 0):
                draw = ImageDraw.Draw(img)
                draw.rectangle((x - 1, y - 1, x + 1, y + 1), 235)
    return img


def get_characters_via_ocr(work_id):
    image_url = rf'https://www.tthfanfic.org/pieimg.php?no={work_id}&mode=scharacters'

    # Send a GET request to the image URL and open the image as a PIL Image object
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
    except Exception as e:
        logger(module_tth_py, f'Error   : {e}')
        return None

    # Use Tesseract OCR to extract text from the image
    crop_area_1 = (1, 310, 398, 478)

    # Define the crop rectangle
    crop_1 = img.crop(crop_area_1)

    # Get rid of transparent border
    crop_area_get_1 = getPointForCrop1(crop_1)
    crop_area_get_2 = getPointForCrop2(crop_1)
    crop_area_2 = (crop_area_get_1[0] + 1, crop_area_get_1[1] + 1, crop_area_get_2[0] - 1, crop_area_get_2[1] - 1)
    crop_2 = crop_1.crop(crop_area_2)
    grey_img = crop_2.convert('L')
    crop_3 = remove_colour_boxes(grey_img)
    ungrey = crop_3.convert('RGB')
    new_size = (ungrey.size[0] * 4, ungrey.size[1] * 4)
    resized_img = ungrey.resize(new_size)
    try:
        work_characters_temp = image_to_string(resized_img).split('\n')
        work_characters_temp = list(filter(None, work_characters_temp))
    except TesseractNotFoundError:
        return "Tesseract OCR Not Installed"
    # Could split at space to prevent weird results

    return tuple(work_characters_temp)


def downloadWorkFromID_tth(workID, title, downloadFormat):
    if downloadFormat not in valid_download_formats_tth:
        logger(module_tth_py, f'Error   : Selected Format for download of TTH_{workID} is {downloadFormat} which is not supported. Changing format to {valid_download_formats_tth[0]}')
        downloadFormat = valid_download_formats_tth[0]

    if downloadFormat == 'HTML':
        urlFormat = 'offlinehtml'
    elif downloadFormat == 'TEXT':
        urlFormat = 'text'
    elif downloadFormat == 'EPUB':
        urlFormat = 'epub'
    elif downloadFormat == 'MOBI':
        urlFormat = 'mobi'

    url_download = f"https://www.tthfanfic.org/wholestory.php?no={workID}&format={urlFormat}"

    cleanTitle = sub(r'[^\w\.\-]', ' ', title)
    fileName = f'TTH_{workID}_{cleanTitle}'
    filePath = join(download_storage_dir, f'{fileName}.{downloadFormat}')

    try:
        content = requests.get(url_download).content
    except Exception as e:
        logger(module_tth_py, f'Error   : Something went wrong downloading TTH_{workID} -- {e}')

    if content == bytes(b''):
        return False
        # raise Exception("Download format is probably incorrect")

    with open(filePath, 'wb') as file:
        file.write(content)
        file.close()

    if isfile(filePath):
        return True


def fetchMetadataFromID_tth(workID):
    response = requests.get(f"https://www.tthfanfic.org/StoryInfo-{workID}")
    soup = BeautifulSoup(response.text, "html.parser")

    storyDetailsTables = soup.find("table", class_="horizontaltable")
    storyRankingsTables = soup.find("table", class_="verticaltable")
    storyChapterTables = soup.find_all("table", class_="verticaltable")

    try:
        get_work_title = storyDetailsTables.find("th", string="Title").parent.find("td").text
    except AttributeError:
        return {'unavailable': '1'}

    logger(module_tth_py, f'Success : Found info for TTH_{workID}')

    try:
        get_work_series = storyDetailsTables.find("th", string="Series").parent.find("td").text
    except AttributeError:
        get_work_series = None

    get_work_summary = storyDetailsTables.find("th", string="Summary").parent.find("td").text
    get_work_authors = storyDetailsTables.find("th", string="Author").parent.find("td").text
    get_work_status = storyDetailsTables.find("th", string="Completed").parent.find("td").text
    get_work_primary_categories = storyDetailsTables.find("th", string="Primary Category").parent.find("td").text
    get_work_classifications = storyDetailsTables.find("th", string="Classifications").parent.find('td')
    get_work_words = storyRankingsTables.find("td", string="Words").parent.select('td')[1].get_text(strip=True)
    get_work_hits = storyRankingsTables.find("td", string="Total Hits").parent.select('td')[1].get_text(strip=True)
    get_work_kudos = storyRankingsTables.find("td", string="Reviews").parent.select('td')[1].get_text(strip=True)
    get_work_chapters = storyDetailsTables.find("th", string="Chapters").parent.find("td").text
    get_work_date_published = storyChapterTables[1].find("td", string="1").parent.select('td')[5].get_text(strip=True)
    get_work_date_updated = storyChapterTables[1].find("td", string=get_work_chapters).parent.select('td')[5].get_text(strip=True)
    get_work_date_edited = storyChapterTables[1].find("td", string=get_work_chapters).parent.select('td')[6].get_text(strip=True)
    get_work_rating = storyDetailsTables.find("th", string="Rating").parent.find("td").text

    get_work_primary_categories = get_work_primary_categories.split('->\xa0')

    get_work_fandoms = get_work_primary_categories[0].rstrip()

    work_tags_temp = []
    temp_split_list = str(get_work_classifications).split('>')
    for x in temp_split_list:
        if '<br/' in x:
            work_tags_temp.append(x.replace('<br/', ''))
        elif '</td' in x:
            work_tags_temp.append(x.replace('\n</td', ''))
    work_tags_temp += get_work_primary_categories
    get_work_tags = tuple(work_tags_temp)

    if len(get_work_primary_categories) > 2:
        if 'Pairing:' in get_work_primary_categories[2]:
            temp_a = get_work_primary_categories[1].replace('-Centered', '')
            temp_b = get_work_primary_categories[2].replace('Pairing: ', '')
            get_work_relationships = f'{temp_a}/{temp_b}'
        else:
            get_work_relationships = None
    else:
        get_work_relationships = None

    work_categories_temp = []
    if get_work_tags:
        if 'Hetero Sex' in get_work_tags:
            work_categories_temp.append('F/M')
        if 'Femslash' in get_work_tags:
            work_categories_temp.append('F/F')
        if 'Slash' in get_work_tags:
            work_categories_temp.append('M/M')
        get_work_categories = tuple(work_categories_temp)
        if not get_work_categories:
            get_work_categories = 'Other'
    else:
        get_work_categories = 'Other'

    work_title = get_work_title
    work_summary = get_work_summary
    work_series = get_work_series
    work_authors = get_work_authors
    work_fandoms = get_work_fandoms
    work_tags = get_work_tags
    work_characters = get_characters_via_ocr(workID)
    work_categories = get_work_categories
    work_relationships = get_work_relationships
    work_warnings = 'Warnings Not Found'
    work_status = get_work_status
    work_rating = get_work_rating
    work_language = 'English'
    work_chapters = get_work_chapters.replace(',', '')
    work_words = get_work_words.replace(',', '')
    work_hits = get_work_hits.replace(',', '')
    work_kudos = get_work_kudos.replace(',', '')
    work_date_edited = datetime.strftime(datetime.strptime(get_work_date_edited, "%d %b %y"), "%Y-%m-%d %H:%M:%S")
    work_date_published = datetime.strftime(datetime.strptime(get_work_date_published, "%d %b %y"), "%Y-%m-%d %H:%M:%S")
    work_date_updated = datetime.strftime(datetime.strptime(get_work_date_updated, "%d %b %y"), "%Y-%m-%d %H:%M:%S")

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


def module_tth():
    pass


if __name__ == '__main__':
    module_tth()
    # https://www.tthfanfic.org/StoryInfo-32730/
    # fetchMetadataFromID_tth(15603)
    print(fetchMetadataFromID_tth(12176))
    # print(fetchMetadataFromID_tth(29228))
    # print(fetchMetadataFromID_tth(32730))
