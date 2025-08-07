from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import status
import logging
from ultralytics import YOLO
from PIL import Image
import io
import os
import log_config 
from fetch_model import Fetch_model

log_config.config_setup()
logger = logging.getLogger(__name__)

model_name = os.getenv("MODEL_NAME")
version = os.getenv("VERSION")
user_id = os.getenv("URI")

MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BY = MAX_FILE_SIZE_MB * 1024 * 1024 
ALLOWED_FILE_TYPE = ("jpg","png","jpeg")

get_model = Fetch_model(user_id)
fetched_model = get_model.channel_model(model_name, version, "best.pt")
run_yolo_model = YOLO(fetched_model, task="detect")

app = FastAPI()

@app.post("/upload")
async def message(file : UploadFile) -> JSONResponse:
    """
    Args:
       file (UploadFile): upload image file through POST request

    Returns:
        JSONResponse: verify file and returns 'Prediction'
    """
    

    is_valid_file = await File_Check(file)
    
    if is_valid_file[0] is not None:
        image = Image.open(io.BytesIO(is_valid_file[0])).convert("RGB")
        logger.info(is_valid_file[1])

        prediction_result = Model_Prediction(image)
        
        return JSONResponse(
            content=prediction_result, 
            status_code= status.HTTP_200_OK
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=is_valid_file[1]
        )

@app.get("/")
def documentation() -> JSONResponse:
    """
    Documentation 
    """
    docs = {"documentation": {
            "/upload": {
                "method": "POST",
                "description": "Takes an image file and returns a prediction.",
                "outputs": {
                "400": "HTTP Bad Request - For large files or invalid data types.",
                "200": [
                    {
                    "Prediction": "Product not found"
                    },
                    {
                    "Prediction": "prediction_results"
                    }
                ],
                "500": {
                    "Prediction": "Failed"
                }
                }
            }
            }
    }
    return JSONResponse(
        content=docs, 
        status_code= status.HTTP_200_OK
    )
   

async def File_Check(file: UploadFile) -> tuple:
    """
    Args:
       file (UploadFiles): uploaded image via POST 
    
    Returns:
       tuple: return 
    
    """
    file_s_msg = f"File content too large. Maximum allowed size is {MAX_FILE_SIZE_MB}MB"
    file_t_msg = f"File type is not allowed. Only {ALLOWED_FILE_TYPE}"
    file_v_msg = f"File is valid" 

    if file.filename.split(".")[-1] in ALLOWED_FILE_TYPE:
        uploaded_file: bytes = await file.read()
        if len(uploaded_file) > MAX_FILE_SIZE_BY:
           logging.warning(file_s_msg)
           return (None, file_s_msg)
        else:
            return (uploaded_file, file_v_msg) 
    logging.warning(file_t_msg)
    return (None, file_t_msg)
    


def Model_Prediction(image: Image) -> dict:
    """
    Args:
       image (Image): takes in image and make 'Prediction' using custom trained YOLO model

    Returns:
        dict : return 'Prediction'

    """
    try:
        results = run_yolo_model(image, 
                    imgsz=1280,       
                    iou=0.5,          
                    conf=0.3,        
                    agnostic_nms=True, 
                    max_det=100)      
        

        class_names = run_yolo_model.names 
        for result in results:
            boxes = result.boxes  
            if boxes is None or boxes.cls.numel() == 0:
                return {
                    "Prediction": "Product not found"
                    }
            prediction_results = dict()

            for box in boxes:
                cls_id = box.cls.item()
                cls_name = class_names[cls_id]
                XYWH = box.xywh[0].tolist()
                conf = box.conf.item()
                if cls_name not in prediction_results:
                    prediction_results[cls_name] = []
                
                prediction_results[cls_name].append((XYWH,conf))
        final_prediction = {
            "Prediction":prediction_results
            }
        
        logger.info(f"Model prediction successful")
        return final_prediction
    
    except Exception as e:
        logger.exception(f"Model prediction failed : {e}")
        return { 
            "Predicton":"Failed"
            }

