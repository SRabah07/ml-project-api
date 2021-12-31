import logging
import pickle
import os
import pandas as pd
from models import StrokeObservation
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder

logger = logging.getLogger(__name__)

STORED_STROKE_MODELS_PATH = os.environ.get('STORED_MODELS_PATH', "./storage/models/stroke")

# FIXME check which columns were used in the stored models and their names. Check the two warning below
# FIXME checl pickle version => Trying to unpickle estimator OneHotEncoder from version 0.24.2 when using version 1.0.1.
# FIXME Trying to unpickle estimator OneHotEncoder from version 0.24.2 when using version 1.0.1.

NUMERICS = ['age', 'avg_glucose_level', 'bmi']

CATEGORICALS = ['gender', 'hypertension', 'heart_disease', 'Residence_type', 'smoking_status']


def make_stroke_prediction(key: str, observation: StrokeObservation):
    dictionary = observation.__dict__
    logger.debug(f"Predict stroke of observation: {dictionary}, using model within key: '{key}'")
    if observation.bmi is None:
        dictionary['bmi_nan'] = 'Non'
    else:
        dictionary['bmi_nan'] = 'Oui'

    df = pd.DataFrame(dictionary, index=[0])
    logger.debug(f"Dataframe columns: {df.columns}: \n {df}")

    # Get the model of the given key
    model = get_model(key)
    logger.debug(f"Loaded Model: {type(model)}")

    results = model.predict(df)
    prediction = "NO" if results[0] == 0 else "YES"
    return "Stroke Attack: " + prediction


def get_model(key):
    path_to_model = f"{STORED_STROKE_MODELS_PATH}/{key}.pickle"
    logger.debug(f"Load model from path:{path_to_model}")
    exist = os.path.exists(path_to_model)
    if not exist:
        raise Exception(f"Model within path={path_to_model} doesn't exist!")

    return pickle.load(open(path_to_model, 'rb'))
