from celery_config import app
import logging
import sqlalchemy
import pandas as pd
import os
from src.utils.config import db_config as config

table_name = 'data'
engine = sqlalchemy.create_engine('mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                                  .format(config['user'], config['password'], config['host'], config['port'],
                                          config['database']))


@app.task
def save_data_from_csv(file_path):
    logging.info('New record save task to run, file path :: ' + file_path)
    try:
        df = pd.read_csv(filepath_or_buffer=file_path)
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    except Exception as e:
        logging.error('Error while dumping file :: {0}, error {1}'.format(file_path, e.__str__()))

    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        logging.info("The file :: " + file_path+" :: does not exist, removed already")

    logging.info('Dumped data successfully from file path :: ' + file_path)
