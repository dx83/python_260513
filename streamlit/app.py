import streamlit as st
from PIL import Image

st.title("제목")

name = st.text_input("이름 입력", "")

if name:
    st.write(name + "님 반갑습니다.")

# 이 폴더에서 cmd
# streamlit run app.py
# Email에서 Enter
# 웹 열림
# 리엑트없이 파이썬 확인

st.title("이미지 업로드 예제")

# 이미지 업로드
uploaded_file = st.file_uploader(
    "이미지를 업로드하세요",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    # 이미지 열기
    image = Image.open(uploaded_file)

    # 이미지 표시
    st.image(image, caption="업로드한 이미지", use_container_width=True)

    # 파일 정보
    st.write("파일명:", uploaded_file.name)
    st.write("파일 타입:", uploaded_file.type)
    st.write("파일 크기:", uploaded_file.size, "byte")
