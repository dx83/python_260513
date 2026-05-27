import numpy as np
from PIL import Image
import io
import joblib
from fastapi import APIRouter, Form, File, UploadFile, Body, Request

router = APIRouter(prefix="/api/predict", tags=["predict"])

@router.post("/number")
async def predict_number(request:Request, file: UploadFile = File(...)):
    try:
        # 1. 이미지 받기
        content = await file.read()

        # 2. 흑백이미지로 변환
        image = Image.open(io.BytesIO(content)).convert("L")

        # 3. 이미지 크기를 28*28로 변환
        image = image.resize((28, 28))

        # 4. 이미지를 배열로 변경
        image_array = np.array(image)
        # 색 반전
        image_array = 255 - image_array

        # 5. (1, 784)로 변경
        input_input = image_array.reshape(1, 784)

        # 6. 예측
        model = request.app.state.image_model
        pred = model.predict(input_input)

        return {"pred": int(pred[0])}

    except Exception as e:
        return {"message": str(e)}

