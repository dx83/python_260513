import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# 클래스 이름 (영어)
CLASS_NAMES = [
    "daisy",
    "dandelion",
    "roses",
    "sunflowers",
    "tulips"
]

# 한글 이름 매핑 사전 추가
KOREAN_NAMES = {
    "daisy": "데이지",
    "dandelion": "민들레",
    "roses": "장미",
    "sunflowers": "해바라기",
    "tulips": "튤립"
}

# 모델 로드
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("../pkl/20260601_flower_efficientnetv2b0.keras")
    return model

model = load_model()

st.title("🌸 Flower Classification")
st.write("꽃 이미지를 업로드하면 종류를 예측합니다.")

uploaded_file = st.file_uploader(
    "이미지 선택",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="업로드 이미지",
        use_container_width=True
    )

    # 전처리
    img = image.resize((224, 224))
    img = np.array(img, dtype=np.float32)

    # EfficientNetV2 입력 전처리
    img = tf.keras.applications.efficientnet_v2.preprocess_input(img)

    img = np.expand_dims(img, axis=0)

    # 추론
    pred = model.predict(img, verbose=0)

    pred_class = np.argmax(pred)
    confidence = float(np.max(pred))

    # 영어 이름 찾기
    eng_name = CLASS_NAMES[pred_class]
    # 한글 이름 변환 (사전에 없으면 영어 이름 그대로 출력)
    kor_name = KOREAN_NAMES.get(eng_name, eng_name)

    st.subheader("예측 결과")

    # 한글 이름으로 변경하여 출력
    st.success(
        f"{kor_name} ({confidence:.2%})"
    )

    st.subheader("클래스별 확률")

    for cls, prob in zip(CLASS_NAMES, pred[0]):
        # 클래스별 확률 목록도 한글로 변경
        kor_cls = KOREAN_NAMES.get(cls, cls)
        st.write(f"{kor_cls}: {prob:.2%}")