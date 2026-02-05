import pandas as pd
import os
from sqlalchemy import create_engine 
import logging
import time

# make logs folder if it does not exist
if not os.path.exists("Logs"):
    os.makedirs("Logs")

# Creating a logger for ingestion_db
logger = logging.getLogger("ingestion_db")
logger.setLevel(logging.DEBUG)
logger.propagate = False   #prevents logs from bubbling up to root

if not logger.handlers:
    fh = logging.FileHandler("Logs/ingestion_db.log", mode="a")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

engine = create_engine('sqlite:///vendor_performance.db')

def ingest_db(df, table_name, engine):
    '''This function will ingest dataframe into database table'''
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)

def load_raw_data():
    '''This function will load the CSVs as dataframe and ingest into db'''
    start = time.time()

    # check if Data folder exists
    if not os.path.exists("Data"):
        raise FileNotFoundError("Data folder not found. Please check folder name: Data")

    for file in os.listdir('Data'):
        if file.endswith(".csv"):
            df = pd.read_csv('Data/'+file)
            logger.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time_taken = (end-start)/60
    logger.info('Ingestion Complete')
    logger.info(f'Total Time Taken: {total_time_taken:.2f} minutes')

if __name__ == '__main__':
    load_raw_data()