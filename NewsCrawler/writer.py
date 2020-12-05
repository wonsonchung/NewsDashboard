import psycopg2.extras
from typing import List, Dict
from NewsCrawler.db_config import CONFIG
import boto3
import json

class Writer(object):

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
        db_con = psycopg2.connect(**CONFIG)
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

    @classmethod
    def get_url_to_crawl(cls, category: int, start_date: str, end_date: str) -> List[List]:
        urls = []
        db_con = psycopg2.connect(**CONFIG)
        db_cur = db_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f''' SELECT category, aid, url FROM news_metadata \
                     WHERE upload_date >= {start_date} and upload_date <= {end_date}\
                     AND category = {category}'''
        db_cur.execute(query)

        result = db_cur.fetchall()
        db_con.rollback()
        return result

    @classmethod
    def write_json_to_s3(cls, category_name: str, value: Dict, file_name: str):

        session = boto3.Session(profile_name='ybigta-conference')
        client = session.client('s3')
        client.put_object(
            Body=str(json.dumps(value)),
            ContentEncoding='utf8',
            Bucket='naver-news-dev',
            Key=f"news_content/{category_name}/{file_name}.json"
        )

