import pandas as pd
import numpy as np
from preprocess import clean_fill_data, preprocess
from common.config import config
import joblib


def make_predictions(input_data: pd.DataFrame) -> np.ndarray:
    #data cleaning
    input_data = clean_fill_data(input_data)
    X = preprocess(input_data,'test')
    model = joblib.load(config['MODEL']['MODEL_PATH'])
    y_pred = model.predict_proba(X)
    return y_pred

if __name__ == '__main__':
    data = pd.read_csv(config['DATA']['PATH'])
    predictions = make_predictions(data.iloc[:,:-1])
    print(predictions)


