import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config("🧠 Face Detection App", layout="centered")
st.title("🧠 Face Detection App (OpenCV + Streamlit)")

# Upload Image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Load Haar Cascade for face detection
@st.cache_resource
def load_face_cascade():
    return cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

face_cascade = load_face_cascade()

# Perform detection
if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(img)

    # Optional Resize if image is too large
    if img_np.shape[1] > 1000:
        img_np = cv2.resize(img_np, (800, int(800 * img_np.shape[0] / img_np.shape[1])))

    img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # More sensitive detection
    faces = face_cascade.detectMultiScale(
        img_gray,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(30, 30)
    )

    st.subheader(f"👁️ Faces Detected: {len(faces)}")

    for (x, y, w, h) in faces:
        cv2.rectangle(img_np, (x, y), (x + w, y + h), (0, 255, 0), 2)

    st.image(img_np, caption="Detected Faces", use_container_width=True)
else:
    st.info("Upload an image to detect faces.")
