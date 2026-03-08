import os
import logging
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from src.utils.schema import CustomerData
from src.utils.services.predict import process_input,predict_customer
from src.utils.logger import setup_logger
from src.utils.exception import AppException
from fastapi.templating import Jinja2Templates
from fastapi import Request
# -----------------------------
# Initialize logging
# -----------------------------
templates = Jinja2Templates(directory="templates")
setup_logger()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(
    title="Customer Churn Prediction",
    version="1.0.0"
)

logger.info("FastAPI application initialized")



# -----------------------------
# Home route
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    try:

        logger.debug("Home route accessed")

        return templates.TemplateResponse(
            "home.html",
            {"request": request}
        )

    except AppException as e:

        logger.error(str(e))

        return HTMLResponse(
            content=f"<h2>Application Error</h2><p>{str(e)}</p>",
            status_code=500
        )

    except Exception as e:

        logger.exception("Unhandled exception in home route")

        return HTMLResponse(
            content="<h2>Unexpected server error</h2>",
            status_code=500
        )  

@app.get("/health")
def health_check():
    return {"status": "ok"}

# -----------------------------
# Processing the input data and displaying the results. 
# -----------------------------


from fastapi.responses import JSONResponse

@app.post("/predict")
def predict(data: CustomerData):

    try:

        input_dict = process_input(data)
        pred, prob = predict_customer(input_dict)

        result = {
            "prediction": int(pred),
            "probability": float(prob)
        }

        logger.info(f"Prediction result: {result}")

        return JSONResponse(content=result)

    except Exception as e:
        logger.exception("Prediction error")

        return JSONResponse(
            status_code=500,
            content={"error": "Prediction failed"}
        )
    
