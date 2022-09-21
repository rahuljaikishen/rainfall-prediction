import os
from sklearn.linear_model import LogisticRegression

config = {
    "MODEL" : {
        "CLASS": LogisticRegression,
        "ARGS":{'random_state' : 0, 'solver':'lbfgs', 'max_iter':1000},
        "MODEL_PATH":"../models/logistic_regression.joblib",
        "SCALER":"../models/scaler.joblib",
        "ENCODER":"../models/oh_encoder.joblib"
    },
    "DATA_PREPROCESS" : {
        "DROP_FEATURES":['Date','Sunshine', 'Evaporation'],
    },
    "DATA" : {
        "PATH":"../data/weatherAUS.csv",
        "INFERENCE_PATH":"../data/inference/",
        "DATA_SAVE_PATH":"../data/"
    },
    "API": {
        "URL":"http://127.0.0.1:8000"
    },
    "DATABASE": {
        "USERNAME":"postgres",
        "PASSWORD":"J@tin15031996",
        "HOSTNAME":"127.0.0.1",
        "PORT":5432,
        "DB_NAME":"rainfall_predictions"
    }
}