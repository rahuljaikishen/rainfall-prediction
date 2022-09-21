import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
import sys 

from common.config import config


def clean_fill_data(input_data):
    #dropping columns
    for col in config['DATA_PREPROCESS']['DROP_FEATURES']:
        if col in input_data.columns:
            input_data = input_data.drop(col,axis=1)
    
    #filling missing values for numerical data
    input_data = fill_numerical(input_data)
    
    #filling missing values for objects
    input_data = fill_object(input_data)
    
    return input_data 

def fill_numerical(input_data):
    for col in input_data.select_dtypes(['int', 'float']):
        input_data[col] = input_data[col].fillna(input_data[col].median())
    return input_data


def fill_object(input_data):
    for col in input_data.select_dtypes('object'):
        input_data[col] = input_data[col].fillna(method='ffill')
    return input_data

def select_feature_and_target(input_data):
    #Assuming target values are either Yes or no and is the last column with the rest of the columns being features
    
    X = input_data.iloc[:,:-1]
    y = input_data.iloc[: , -1].apply(lambda x: 1 if x=='yes' or x=='Yes' else 0)
    
    return X, y

def preprocess(input_data, stage='train'):
    processed_data = input_data.copy()
    processed_data = scale_numerical_data(processed_data, stage)
    processed_data = encode_categorical_data(processed_data, stage)
    return processed_data    

def scale_numerical_data(data, stage):
    numerical_columns = get_numerical_columns(data)
    if stage == 'train':
        scaler = StandardScaler()
        scaler.fit(data[numerical_columns])
        joblib.dump(scaler, config['MODEL']['SCALER'])
    else:
        scaler = joblib.load(config['MODEL']['SCALER'])

    standarized_data = scaler.transform(data[numerical_columns])
    standarized_data_df = pd.DataFrame(standarized_data,
                                       columns=numerical_columns, index=data.index)
    scaled_data = data.copy().drop(columns=numerical_columns, axis=1).join(standarized_data_df)

    return scaled_data

def encode_categorical_data(data, stage):
    categorical_columns = get_categorical_columns(data)
    if stage == 'train':
        encoder = OneHotEncoder(sparse=False)
        encoder.fit(data[categorical_columns])
        joblib.dump(encoder, config['MODEL']['ENCODER'])
    else:
        encoder = joblib.load(config['MODEL']['ENCODER'])
    
    categorical_data_encoded = encoder.transform(data[categorical_columns])
    feature_names = encoder.get_feature_names_out(input_features=categorical_columns)
    categorical_data_encoded_df = pd.DataFrame(categorical_data_encoded,
                                       columns=feature_names, index=data.index)
    encoded_data = data.copy().drop(columns=categorical_columns, axis=1).join(categorical_data_encoded_df)
    
    return encoded_data

def get_categorical_columns(input_data):
    categorical_columns = list(input_data.select_dtypes(include='object').columns)
    return categorical_columns

def get_numerical_columns(input_data):
    numerical_columns = list(input_data.select_dtypes(include=['int', 'float']).columns)
    return numerical_columns



