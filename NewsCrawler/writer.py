import psycopg2.extras
from typing import List, Dict
import s3fs

class Writer(object):

    host = 'ybigta-news.cga4jkz7xhwb.ap-northeast-2.rds.amazonaws.com'
    user = 'news'
    pwd = 'ybigta1234'
    database = 'dev'
    port = 5432

    @classmethod
    def to_db_value(cls, values: List[Dict]) -> List[str]:
        values_to_insert = []
        for row in values:
            for key in row:
                temp = row[key]
                row[key] = f"'{temp}'"

            value = f''' ({(",".join(list(row.values()))).strip('"')}) '''
            values_to_insert.append(value)

        return values_to_insert

    @classmethod
    def insert_to_db(cls, table: str, values: List[str]):
        query = f''' insert into {table} values {','.join(values)}'''
        db_con = psycopg2.connect(database=cls.database, host=cls.host, user=cls.user, \
                                  password=cls.pwd, port=cls.port)
        db_cur = db_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        db_cur.execute(query)
        db_con.commit()

    @classmethod
    def insert_values_to_db(cls, table: str, values: List[Dict]):
        try:
            values_to_insert = cls.to_db_value(values)
            cls.insert_to_db(table, values_to_insert)
        except Exception as e:
            print(e, '\n==>', [x['aid'] for x in values])
