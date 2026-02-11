from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, HTMLResponse
from uvicorn import run as app_run

from typing import Optional

#importing constants 

from src.constants import APP_HOST, APP_PORT
from src.pipeline.prediction_pipeline import VehicleData, VehicleDataClassifier
from src.pipeline.training_pipeline import TrainPipeline

#initialize app

app = FastAPI()
# mount static directory for serving static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

#allow all origins for CORS (Cross-Origin Resource Sharing)
origins = ["*"]

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    '''Class to represent the form data for vehicle insurance prediction'''
    def __init__(self, request: Request):
        self.request: Request = request
        self.Gender: Optional[int] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age_lt_1_Year: Optional[int] = None
        self.Vehicle_Age_gt_2_Years: Optional[int] = None
        self.Vehicle_Damage_Yes: Optional[int] = None

    async def get_vehicle_details(self):
        '''Method to extract vehicle details from the form data'''
        form_data = await self.request.form()
        self.Gender = form_data.get("Gender")
        self.Age = int(form_data.get("Age"))
        self.Driving_License = int(form_data.get("Driving_License"))
        self.Region_Code = int(form_data.get("Region_Code"))
        self.Previously_Insured = int(form_data.get("Previously_Insured"))
        self.Annual_Premium = float(form_data.get("Annual_Premium"))
        self.Policy_Sales_Channel = int(form_data.get("Policy_Sales_Channel"))
        self.Vintage = int(form_data.get("Vintage"))
        self.Vehicle_Age_lt_1_Year = int(form_data.get("Vehicle_Age_lt_1_Year"))
        self.Vehicle_Age_gt_2_Years = int(form_data.get("Vehicle_Age_gt_2_Years"))
        self.Vehicle_Damage_Yes = int(form_data.get("Vehicle_Damage_Yes"))

#Route to render the home page with the form
@app.get("/", tags=['authentication'])
async def index(request: Request):
    '''Route to render the home page with the form'''
    return templates.TemplateResponse("index.html", {"request": request, "context": "Rendering"})

#Route to train
@app.get("/train")
async def trainRouteClient():
    '''Route to trigger the training pipeline'''
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response(content="Training successful!!", media_type="text/plain")
    except Exception as e:
        return Response(content=f"Error occurred during training: {str(e)}", media_type="text/plain")

#Route to handle form submission and make predictions
@app.post("/")
async def predictRouteClient(request: Request):
    '''endpoint to recieve the data, process it and make prediction'''
    try:
        form = DataForm(request)
        await form.get_vehicle_details()
        vehicle_data = VehicleData(
            Gender = form.Gender,
            Age = form.Age,
            Driving_License = form.Driving_License,
            Region_Code = form.Region_Code,
            Previously_Insured = form.Previously_Insured,
            Annual_Premium = form.Annual_Premium,
            Policy_Sales_Channel = form.Policy_Sales_Channel,
            Vintage = form.Vintage,
            Vehicle_Age_lt_1_Year = form.Vehicle_Age_lt_1_Year,
            Vehicle_Age_gt_2_Years = form.Vehicle_Age_gt_2_Years,
            Vehicle_Damage_Yes = form.Vehicle_Damage_Yes
        )
        vehicle_df = vehicle_data.get_vehicle_input_data_frame()
        model_predictor = VehicleDataClassifier()
        value = model_predictor.predict(dataframe=vehicle_df)[0]
        status = "Insured - Response: YES" if value == 1 else "Not Insured - Response: NO"

        return templates.TemplateResponse("index.html", {"request": request, "context": status})
    except Exception as e:
        return {"status": False, "error": f"{e}"}

if __name__ == "__main__":
    '''Main function to run the FastAPI app'''
    app_run(app, host=APP_HOST, port=APP_PORT)



