import pandas as pd
from airflow.decorators import dag,task
from airflow.utils.dates import timedelta
from pendulum import today
from airflow.hooks.postgres_hook import PostgresHook
import logging
import os 
from rainfall_predictions.inference import make_predictions

logger = logging.getLogger("airflow.task")

@dag(
    dag_id="data_ingestion_dag",
    description="To check db for new testing data",
    schedule_interval=timedelta(minutes=5),
    start_date=today().add(hours=-1) 
)

def make_data(dates, predictions):
    predictions_df = pd.DataFrame(predictions[:, 1].reshape(-1, 1),
                                  columns=['Dates','Rainfall predicted'], index=dates.index)
    return dates.join(predictions_df)

def get_data():
    @task
    def get_db_data():
        query = "select file_location from rainfall_test_data where processed = 0"
        pg_hook = PostgresHook(
            postgres_conn_id = 'postgres_db'
        )
        pg_conn = pg_hook.get_conn()
        cursor = pg_conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        value = result[0][0]
        return value

    @task
    def get_file(file_name):
        
        data = pd.read_csv(file_name)
        predictions = make_predictions(data)
        formatted_data = make_data(data[['Dates']],predictions)

        query_insert = "insert into rainfall_predictions(`date`,`prediction`) values"
        for index, row in formatted_data.iterrows():
            query_insert += "('"+str(row['Dates'])+"',"+"'"+str(row['predicted'])+"')"
            if index != (formatted_data.shape[0]-1):
                query_insert += ','
        
        pg_hook = PostgresHook(
            postgres_conn_id = 'postgres_db'
        )
        
        pg_conn = pg_hook.get_conn()
        cursor = pg_conn.cursor()
        cursor.execute(query_insert)

        query_update = "update rainfall_test_data set processed = 1  where file_location = '"+file_name+"'"
        pg_conn = pg_hook.get_conn()
        cursor = pg_conn.cursor()
        cursor.execute(query_update)
        return file_name

    data = get_db_data()
    get_file_data = get_file(data)
    return get_file_data

get_data = get_data()