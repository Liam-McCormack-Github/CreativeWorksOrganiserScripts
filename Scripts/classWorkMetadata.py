import sqlite3
from sqlite3 import Error
from dbConnect import dbConnect
from constants import WorkMetadata_py, https
from module_ao3 import host_ao3, url_indicates_ao3, fetchMetadataFromID_ao3, downloadWorkFromID_ao3
from module_tth import host_tth, url_indicates_tth, fetchMetadataFromID_tth, downloadWorkFromID_tth
from module_ffn import host_ffn, url_indicates_ffn, fetchMetadataFromID_ffn, downloadWorkFromID_ffn
from logger import logger


class WorkMetadata:
    def getCleanURL(self):
        if self.host == host_ao3:
            cleanURl = fr'{https}{url_indicates_ao3[0]}{self.work_id}'
        elif self.host == host_tth:
            cleanURl = fr'{https}{url_indicates_tth[0]}{self.work_id}'
        elif self.host == host_ffn:
            cleanURl = fr'{https}{url_indicates_ffn[0]}{self.work_id}'
        else:
            return None
        return cleanURl

    def getDataAsDict(self):
        workData = {'object_id': self.object_id,
                    'host': self.host,
                    'work_id': self.work_id,
                    'url': self.url,
                    'metadata': self.metadata,
                    'unavailable': self.unavailable,
                    'favourite': self.favourite,
                    'saved': self.saved,
                    'entry_date': self.entry_date,
                    'user_tags': self.user_tags,
                    'title': self.title,
                    'series': self.series,
                    'authors': self.authors,
                    'summary': self.summary,
                    'fandoms': self.fandoms,
                    'tags': self.tags,
                    'characters': self.characters,
                    'categories': self.categories,
                    'relationships': self.relationships,
                    'warnings': self.warnings,
                    'status': self.status,
                    'rating': self.rating,
                    'language': self.language,
                    'chapters': self.chapters,
                    'words': self.words,
                    'hits': self.hits,
                    'kudos': self.kudos,
                    'date_edited': self.date_edited,
                    'date_published': self.date_published,
                    'date_updated': self.date_updated}
        return workData

    def updateWorkInDB(self, workData):
        conn = dbConnect(WorkMetadata_py, True)
        c = conn.cursor()
        update = ','.join([f'{k}=?' for k in workData.keys()])
        query_sql = f'UPDATE IndexData SET {update} WHERE object_id="{self.object_id}";'
        query_data = [workData[k] for k in workData.keys()]
        try:
            c.execute(query_sql, query_data)
            conn.commit()
            logger(WorkMetadata_py, f'Success : Updated {self.object_id}')
            return True
        except sqlite3.IntegrityError:
            logger(WorkMetadata_py, f'Dupe ID : {self.object_id}')
            return False
        except Error as e:
            logger(WorkMetadata_py, f'Error   : {e}')
            return False

    def insertWorkInDB(self):
        conn = dbConnect(WorkMetadata_py, True)
        c = conn.cursor()

        query_sql = '''INSERT OR IGNORE INTO "IndexData" ("object_id",
                                                           "host",
                                                           "work_id",
                                                           "url",
                                                           "metadata",
                                                           "unavailable",
                                                           "title",
                                                           "series",
                                                           "authors",
                                                           "summary",
                                                           "fandoms",
                                                           "tags",
                                                           "characters",
                                                           "categories",
                                                           "relationships",
                                                           "warnings",
                                                           "status",
                                                           "rating",
                                                           "language",
                                                           "chapters",
                                                           "words",
                                                           "hits",
                                                           "kudos",
                                                           "date_edited",
                                                           "date_published",
                                                           "date_updated") 
                                                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''

        query_data = (self.object_id,
                      self.host,
                      self.work_id,
                      self.url,
                      self.metadata,
                      self.unavailable,
                      self.title,
                      self.series,
                      self.authors,
                      self.summary,
                      self.fandoms,
                      self.tags,
                      self.characters,
                      self.categories,
                      self.relationships,
                      self.warnings,
                      self.status,
                      self.rating,
                      self.language,
                      self.chapters,
                      self.words,
                      self.hits,
                      self.kudos,
                      self.date_edited,
                      self.date_published,
                      self.date_updated)

        c.execute(query_sql, query_data)
        conn.commit()
        logger(WorkMetadata_py, f'Success : Executed SQL with = {query_data}')

    def queryDB(self):
        conn = dbConnect(WorkMetadata_py, True)
        c = conn.cursor()
        c.execute(f'''SELECT "object_id",
                             "host",
                             "work_id",
                             "url",
                             "metadata",
                             "unavailable",
                             "favourite",
                             "saved",
                             "entry_date",
                             "user_tags",
                             "title",
                             "series",
                             "authors",
                             "summary",
                             "fandoms",
                             "tags",
                             "characters",
                             "categories",
                             "relationships",
                             "warnings",
                             "status",
                             "rating",
                             "language",
                             "chapters",
                             "words",
                             "hits",
                             "kudos",
                             "date_edited",
                             "date_published",
                             "date_updated"   
                      FROM IndexData 
                      WHERE object_id="{self.object_id}";''')
        rows = c.fetchall()
        if rows:
            return rows[0]
        else:
            logger(WorkMetadata_py, f'Error : {self.object_id} Not found in Database. ')
            self.insertWorkInDB()
            self.queryDB()

    def updateClassFromDB(self):
        queryData = list(self.queryDB())

        for i, x in enumerate(queryData):
            if x is None:
                x = ''
                queryData[i] = x
            if type(x) != int:
                if '\n' in x:
                    queryData[i] = tuple(x.split('\n'))

        self.object_id = queryData[0]
        self.host = queryData[1]
        self.work_id = queryData[2]
        self.url = queryData[3]
        self.metadata = queryData[4]
        self.unavailable = queryData[5]
        self.favourite = queryData[6]
        self.saved = queryData[7]
        self.entry_date = queryData[8]
        self.user_tags = queryData[9]
        self.title = queryData[10]
        self.series = queryData[11]
        self.authors = queryData[12]
        self.summary = queryData[13]
        self.fandoms = queryData[14]
        self.tags = queryData[15]
        self.characters = queryData[16]
        self.categories = queryData[17]
        self.relationships = queryData[18]
        self.warnings = queryData[19]
        self.status = queryData[20]
        self.rating = queryData[21]
        self.language = queryData[22]
        self.chapters = queryData[23]
        self.words = queryData[24]
        self.hits = queryData[25]
        self.kudos = queryData[26]
        self.date_edited = queryData[27]
        self.date_published = queryData[28]
        self.date_updated = queryData[29]
        return f'Found   : {self.object_id}'

    def downloadWorkViaModules(self, downloadFormat='HTML'):

        self.updateClassFromDB()

        if self.host == host_ao3:
            workDownloaded = downloadWorkFromID_ao3(self.work_id, self.title, downloadFormat)
        elif self.host == host_tth:
            workDownloaded = downloadWorkFromID_tth(self.work_id, self.title, downloadFormat)
        elif self.host == host_ffn:
            workDownloaded = downloadWorkFromID_ffn(self.work_id, self.title, downloadFormat)
        else:
            return None

        if workDownloaded:
            self.saved = '1'
        else:
            self.saved = '0'

        data = self.getDataAsDict()
        for i, x in enumerate(data.keys()):
            if type(data[x]) == tuple:
                test = "\n".join(data[x])
                data[x] = test
        self.updateWorkInDB(data)

    def getMetadataViaModules(self):

        if self.host == host_ao3:
            workData = fetchMetadataFromID_ao3(self.work_id)
        elif self.host == host_tth:
            workData = fetchMetadataFromID_tth(self.work_id)
        elif self.host == host_ffn:
            workData = fetchMetadataFromID_ffn(self.work_id)
        else:
            return None

        self.updateClassFromDB()

        self.metadata = workData['metadata'] if workData.get('metadata') else self.metadata
        self.unavailable = workData['unavailable'] if workData.get('unavailable') else self.unavailable
        self.favourite = workData['favourite'] if workData.get('favourite') else self.favourite
        self.saved = workData['saved'] if workData.get('saved') else self.saved
        self.user_tags = workData['user_tags'] if workData.get('user_tags') else self.user_tags

        self.title = workData['title'] if workData.get('title') else self.title
        self.summary = workData['summary'] if workData.get('summary') else self.summary
        self.series = workData['series'] if workData.get('series') else self.series
        self.authors = workData['authors'] if workData.get('authors') else self.authors
        self.fandoms = workData['fandoms'] if workData.get('fandoms') else self.fandoms
        self.tags = workData['tags'] if workData.get('tags') else self.tags
        self.characters = workData['characters'] if workData.get('characters') else self.characters
        self.categories = workData['categories'] if workData.get('categories') else self.categories
        self.relationships = workData['relationships'] if workData.get('relationships') else self.relationships
        self.warnings = workData['warnings'] if workData.get('warnings') else self.warnings
        self.status = workData['status'] if workData.get('status') else self.status
        self.rating = workData['rating'] if workData.get('rating') else self.rating
        self.language = workData['language'] if workData.get('language') else self.language
        self.chapters = workData['chapters'] if workData.get('chapters') else self.chapters
        self.words = workData['words'] if workData.get('words') else self.words
        self.hits = workData['hits'] if workData.get('hits') else self.hits
        self.kudos = workData['kudos'] if workData.get('kudos') else self.kudos
        self.date_edited = workData['date_edited'] if workData.get('date_edited') else self.date_edited
        self.date_published = workData['date_published'] if workData.get('date_published') else self.date_published
        self.date_updated = workData['date_updated'] if workData.get('date_updated') else self.date_updated

        data = self.getDataAsDict()
        for i, x in enumerate(data.keys()):
            if type(data[x]) == tuple:
                test = "\n".join(data[x])
                data[x] = test
        self.updateWorkInDB(data)

    def __init__(self, workData):
        if workData.get('object_id') is None:
            logger(WorkMetadata_py, 'object_id cannot be None')
            return

        # NOT NULL
        self.object_id = workData['object_id']
        self.host = self.object_id.split('_')[0]
        if self.host not in (host_ao3, host_ffn, host_tth):
            logger(WorkMetadata_py, f'Error : {self.host} is not supported.')
            return
        self.work_id = self.object_id.split('_')[1]
        self.url = self.getCleanURL()
        if self.url is None:
            return
        self.metadata = workData['metadata'] if workData.get('metadata') else 0
        self.unavailable = workData['unavailable'] if workData.get('unavailable') else 0
        self.favourite = workData['favourite'] if workData.get('favourite') else 0
        self.saved = workData['saved'] if workData.get('saved') else 0
        self.entry_date = workData['entry_date'] if workData.get('entry_date') else ''
        self.user_tags = workData['user_tags'] if workData.get('user_tags') else 'null'

        # CAN BE NULL
        self.title = workData['title'] if workData.get('title') else ''
        self.series = workData['series'] if workData.get('series') else ''
        self.authors = workData['authors'] if workData.get('authors') else ''
        self.summary = workData['summary'] if workData.get('summary') else ''
        self.fandoms = workData['fandoms'] if workData.get('fandoms') else ''
        self.tags = workData['tags'] if workData.get('tags') else ''
        self.characters = workData['characters'] if workData.get('characters') else ''
        self.categories = workData['categories'] if workData.get('categories') else ''
        self.relationships = workData['relationships'] if workData.get('relationships') else ''
        self.warnings = workData['warnings'] if workData.get('warnings') else ''
        self.status = workData['status'] if workData.get('status') else ''
        self.rating = workData['rating'] if workData.get('rating') else ''
        self.language = workData['language'] if workData.get('language') else ''
        self.chapters = workData['chapters'] if workData.get('chapters') else ''
        self.words = workData['words'] if workData.get('words') else ''
        self.hits = workData['hits'] if workData.get('hits') else ''
        self.kudos = workData['kudos'] if workData.get('kudos') else ''
        self.date_edited = workData['date_edited'] if workData.get('date_edited') else ''
        self.date_published = workData['date_published'] if workData.get('date_published') else ''
        self.date_updated = workData['date_updated'] if workData.get('date_updated') else ''
        # Check stuff
        self.queryDB()


def main():
    new_work = WorkMetadata({'object_id': 'FFN_5410629'})
    print(new_work.title)
    # print(new_work.saved)
    # print(new_work.downloadWorkViaModules())
    # print(new_work.saved)
    # new_work.updateWorkInDB({'tags': 'AO3_43715991'})
    # print(new_work.tags)
    # print(new_work.updateClassFromDB())
    # print(new_work.tags)


if __name__ == '__main__':
    main()
