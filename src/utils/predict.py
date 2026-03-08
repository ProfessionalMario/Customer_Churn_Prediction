import joblib
import pandas as pd

# Load model, scaler, and training columns
model = joblib.load("models/churn_model.pkl")
scaler = joblib.load("models/scaler.pkl")
model_features = joblib.load("models/model_features.pkl")

num_cols = ["SeniorCitizen", "tenure", "MonthlyCharges"]

def predict_customer(data):
    df = pd.DataFrame([data])

    # enforce training schema
    df = df.reindex(columns=model_features, fill_value=0)
    
    # scale numeric columns
    df[num_cols] = scaler.transform(df[num_cols])

    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    return pred, prob

if __name__ == "__main__":
    # Example customer: matches your model features
    sample_customer = {
        "SeniorCitizen": 0,
        "tenure": 12,
        "MonthlyCharges": 10.0,
        "gender_Male": 1,
        "Partner_Yes": 0,
        "Dependents_Yes": 1,
        "PhoneService_Yes": 1,
        "MultipleLines_No phone service": 0,
        "MultipleLines_Yes": 1,
        "InternetService_Fiber optic": 1,
        "InternetService_No": 0,
        "OnlineSecurity_No internet service": 0,
        "OnlineSecurity_Yes": 0,
        "OnlineBackup_No internet service": 0,
        "OnlineBackup_Yes": 1,
        "DeviceProtection_No internet service": 0,
        "DeviceProtection_Yes": 1,
        "TechSupport_No internet service": 0,
        "TechSupport_Yes": 0,
        "StreamingTV_No internet service": 0,
        "StreamingTV_Yes": 1,
        "StreamingMovies_No internet service": 0,
        "StreamingMovies_Yes": 1,
        "Contract_One year": 0,
        "Contract_Two year": 1,
        "PaperlessBilling_Yes": 1,
        "PaymentMethod_Credit card (automatic)": 0,
        "PaymentMethod_Electronic check": 1,
        "PaymentMethod_Mailed check": 0
    }

    pred, prob = predict_customer(sample_customer)
    print(f"Prediction: {'Churn' if pred == 1 else 'No Churn'}")
    print(f"Probability of Churn: {prob:.2f}")
