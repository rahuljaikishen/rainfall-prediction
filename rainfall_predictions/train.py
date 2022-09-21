import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_log_error
from preprocess import clean_fill_data, select_feature_and_target, preprocess
import sys
from common.config import config



def build_model(data: pd.DataFrame) -> dict[str, str]:
    #data cleaning
    print(data.dtypes)
    data = clean_fill_data(data)

    #data identification
    X_train, X_test, y_train, y_test = get_train_test_data(data)
    #data encoding and scaling
    X_train = preprocess(X_train)
    model = get_fitted_model(X_train,y_train)

    X_test = preprocess(X_test,'test')
    y_pred = model.predict(X_test)
    rmsle = compute_rmsle(y_test, y_pred)
    accuracy = compute_accuracy(y_test, y_pred)
    return {'accuracy':accuracy, 'rmsle':rmsle}
    
def get_train_test_data(data : pd.DataFrame):
    #select feature and traget variables
    X, y = select_feature_and_target(data)
    X_train, X_test, y_train, y_test = train_test_split(X , y, test_size=0.2, random_state=0)
    return X_train, X_test, y_train, y_test

def get_fitted_model(X_train,y_train):
    model = config['MODEL']['CLASS'](**config['MODEL']['ARGS'])
    model.fit(X_train, y_train)
    joblib.dump(model, config['MODEL']['MODEL_PATH'])
    return model

def compute_rmsle(y_test: np.ndarray, y_pred: np.ndarray, precision: int = 2) -> float:
    rmsle = np.sqrt(mean_squared_log_error(y_test, y_pred))
    return round(rmsle, precision)

def compute_accuracy(y_test: np.ndarray, y_pred: np.ndarray, precision: int=2 ) -> float:
    accuracy= accuracy_score(y_test,y_pred)
    return round(accuracy, precision)

if __name__ == '__main__':
    data_r = pd.read_csv(config['DATA']['PATH'])
    score = build_model(data_r)
    print(score)
