from fastapi import Depends, FastAPI, UploadFile, Request
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse
from typing import Union
from inference import make_predictions
import pandas as pd
import json
from common.db import write_data, read_data
import time
from common.config import config
import shutil


def validate_headers():
    return {'status': True}


app = FastAPI()

router = InferringRouter()


def make_data(dates, predictions):
    print(predictions)
    predictions_df = pd.DataFrame(predictions[:, 1].reshape(-1, 1),
                                  columns=['Rainfall predicted'], index=dates.index)
    return dates.join(predictions_df)

def check_date_exists(prediction_date):
    query = "SELECT prediction from rainfall_predicted_value where date = '"+prediction_date+"'"
    prediction  = read_data(query)
    return prediction

@cbv(router)
class Api:
    valid_request: dict = Depends(validate_headers)
    response_code: int = 200
    response_data: dict = {'data': [], 'msg': ''}

    # def __init__(self):
    #     if not self.valid_request['status']:
    #         self.response_code = 401
    #         self.response_data['msg'] = 'Un-authorized Access'
    #         self.respond_api()

    def save_test_data(self, csv_file):
        t = int(time.time())
        file_name = "weather-"+str(t)+".csv"
        file_location = config['DATA']['DATA_SAVE_PATH']+file_name
        csv_file.to_csv(file_location, sep=',', index=False)
        q = "INSERT INTO rainfall_test_data(created_on, file_location, processed) VALUES ('2022-06-19','"+file_name+"' , 0);"
        write_data(q)


    @router.post("/predictions")
    async def predictions(self, request: Request, file: Union[UploadFile, None] = None):
        form = await request.form()
        contents = form["upload_file"].file
        data = pd.read_csv(contents)
        print(data.head())
        predictions = make_predictions(data.iloc[:, :-1])
        dataframe = make_data(data[['Date']], predictions)
        self.response_data = dataframe.to_json(orient='records')
        self.save_test_data(data)
        return self.respond_api()

    @router.post("/predict_rain")
    async def get_rain_prediction(self, request: Request):
        body = await request.body()
        json_body = json.loads(body)
        date_exists = check_date_exists(json_body['Date'])
        if len(date_exists) == 0:
            data = pd.json_normalize(json_body)
            predictions = make_predictions(data)
            self.response_data = {
                "msg": "There is a "+str(predictions[0 : 1]*100)+"% of chance of rain on "+json_body['Date']
            }
        else:
            self.response_data = {
                "msg": "There is a "+str(date_exists['prediction']*100)+"% of chance of rain on "+json_body['Date']
            }
        print(self.response_data)
        return self.respond_api()

    def respond_api(self):
        return JSONResponse(content=self.response_data, status_code=self.response_code)


app.include_router(router)
