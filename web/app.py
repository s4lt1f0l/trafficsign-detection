import streamlit as st
from ultralytics import YOLO
from PIL import Image, ImageOps
import numpy as np

st.set_page_config(page_title="Traffic Sign Recognition", page_icon="🚦")

st.title("🚦 Traffic Sign Recognition - HCMUS")
st.write("Sinh viên: Đào Quốc Tuấn - 23120392 & Nguyễn Lê Tân Tiến - 23120369")

@st.cache_resource
def load_model():
    return YOLO("weights/best_yolo.pt")

model = load_model()

file = st.sidebar.file_uploader("Upload ảnh biển báo", type=['jpg', 'jpeg', 'png'])

if file:
    # Load and fix orientation
    img = Image.open(file).convert("RGB")
    img = ImageOps.exif_transpose(img)
    
    # Display original image
    st.image(img, caption="Ảnh gốc", use_container_width=True)
    
    # Predict
    with st.spinner('Đang xử lý...'):
        # Pass PIL image directly - ultralytics handles conversion better
        results = model.predict(img, conf=0)
        
        # Check if detections exist
        if len(results[0].boxes) > 0:
            # Get the box with highest confidence
            top_box = results[0].boxes[0]
            max_conf = float(top_box.conf[0])
            
            # If multiple detections, find the true max
            for box in results[0].boxes:
                if float(box.conf[0]) > max_conf:
                    top_box = box
                    max_conf = float(box.conf[0])
            
            cls = int(top_box.cls[0])
            name = model.names[cls]
            
            # Display only text result
            st.markdown(f"### Kết quả dự đoán: **{name}**")
            st.write(f"Độ tin cậy: {max_conf:.2%}")
        else:
            st.warning("Không tìm thấy biển báo nào trong ảnh.")
else:
    st.info("Vui lòng tải lên một hình ảnh từ thanh bên để bắt đầu.")