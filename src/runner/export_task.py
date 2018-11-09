import os

from celery_config import app
import logging
import sqlalchemy
import MySQLdb
import pandas as pd
from src.utils import constant
from src.utils.config import db_config as config

table_name = 'data'
engine = sqlalchemy.create_engine('mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4'
                                  .format(config['user'], config['password'], config['host'], config['port'],
                                          config['database']))


@app.task(bind=True)
def export_data_wrt_dates(self, d1, d2):
    if d2 is None:
        logging.info('Export request for date ' + d1)
        query = 'SELECT * FROM {0} WHERE DATE(`order_purchase_timestamp`) = "{1}"'.format(table_name, d1)
        logging.info('Querying database for query :: {0}'.format(query))

    else:
        logging.info('Export request for date range ' + d1 + ' :: ' + d2)
        query = 'SELECT * FROM {0} WHERE (DATE(`order_purchase_timestamp`) BETWEEN "{1}" AND "{2}")'\
            .format(table_name, d1, d2)
        logging.info('Querying database for query :: {0}'.format(query))

    task_id = self.request.id
    file_path = os.path.join(constant.EXPORT_DIR, task_id + '.csv')
    pd.read_sql(query, engine).to_csv(path_or_buf=file_path)
    logging.info('Dumped data into csv file for task :: {0}, at {1}'.format(task_id, file_path))
