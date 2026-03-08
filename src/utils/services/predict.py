import logging
from src.utils.exception import AppException
import joblib
import pandas as pd

logger = logging.getLogger(__name__)


# Load model, scaler, and training columns
model = joblib.load("models/churn_model.pkl")
scaler = joblib.load("models/scaler.pkl")
model_features = joblib.load("models/model_features.pkl")
num_cols = ["SeniorCitizen", "tenure", "MonthlyCharges"]



def process_input(data):

    try:

        logger.debug("Processing input schema")

        input_dict = data.model_dump()

        # logger.debug(f"Input dictionary: {input_dict}")

        return input_dict

    except Exception as e:

        logger.exception("Input processing failed")

        raise AppException("Error processing input") from e


def build_feature_vector(data_dict):

    df = pd.DataFrame([data_dict])

    # one-hot encode categorical variables
    df = pd.get_dummies(df)

    # align to training feature order
    df = df.reindex(columns=model_features, fill_value=0)

    return df



def predict_customer(data_dict):

    # raw input → dataframe
    df = pd.DataFrame([data_dict])

    # one-hot encode categorical variables
    df = pd.get_dummies(df)

    # align with training feature order
    df = df.reindex(columns=model_features, fill_value=0)

    # convert booleans to integers
    df = df.replace({True: 1, False: 0})

    # ensure numeric dtype
    df = df.astype(float)

    # scale numeric columns
    df[num_cols] = scaler.transform(df[num_cols])
    # print(df)
    pred = int(model.predict(df)[0])
    prob = float(model.predict_proba(df)[0][1])
    return pred, prob