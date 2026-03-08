from pydantic import BaseModel


class CustomerData(BaseModel):

    Gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int | None = None
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float