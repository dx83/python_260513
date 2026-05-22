from fastapi import APIRouter, Body
import numpy as np
import joblib

router = APIRouter(prefix="/api/fish", tags=["fish"])

# 모델읽기
model = None

# 모델 읽기 (1번만 읽기)
@router.on_event("startup")
def load_model():
    global model
    model = joblib.load("./pkl/20260519_lasso.joblib")


# 127.0.0.1:8000/api/fish/predict
# { "length": 25.4, "width": 4.02, "height": 11.52}
@router.post("/predict")
async def predict_fish(
    length:float = Body(...),
    width:float = Body(...),
    height:float = Body(...)
):
    try:
        # 필요시 DB연동 가능
        sample = np.array([[length, width, height]])
        pred = model.predict(sample)
        return {"predict": pred[0]}
    except Exception as e:
        return {"message": str(e)}

