import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 1. โหลดสมองกล AI ที่เราเทรนไว้
model = joblib.load('biomass_ai_model.pkl')

# 2. ตั้งค่าหน้าตาเว็บแอปพลิเคชัน
st.set_page_config(page_title="Biomass AI Optimizer", page_icon="🌱", layout="centered")

st.title("🌱 AI Platform for Biomass Hydrolysis")
st.write("### ระบบปัญญาประดิษฐ์เพื่อทำนายและเพิ่มประสิทธิภาพการย่อยสลายชีวมวล")
st.write("พัฒนาโดยใช้โมเลกุล Machine Learning เพื่อคำนวณผลผลิตตามหลักเคมีสีเขียว (Green Chemistry)")
st.write("---")

# 3. สร้างส่วนควบคุมในแถบด้านข้าง (Sidebar)
st.sidebar.header("🎛️ ปรับสภาวะทางเคมี (Input)")

# ตัวเลือกชนิดของกรด
acid_choice = st.sidebar.selectbox(
    "ชนิดของกรดที่ใช้ย่อย (Acid Type)", 
    options=[1, 2], 
    format_func=lambda x: "กรดอินทรีย์ / กรดอ่อน (Citric/Oxalic Acid)" if x==1 else "กรดอนินทรีย์ / กรดแก่ (HCl/H2SO4)"
)

# สไลเดอร์ปรับค่าต่างๆ
acid_conc = st.sidebar.slider("ความเข้มข้นของกรด (%)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
temp = st.sidebar.slider("อุณหภูมิในปฏิกิริยา (°C)", min_value=40, max_value=150, value=100, step=5)
time = st.sidebar.slider("ระยะเวลาที่ใช้ย่อย (นาที)", min_value=10, max_value=180, value=60, step=5)

# 4. ส่วนคำนวณและแสดงผลลัพธ์
st.write("### 🔮 ผลการประเมินและทำนายโดย AI")

# สร้างโครงสร้างข้อมูลให้เหมือนกับตอนที่ใช้เทรน AI
input_data = np.array([[acid_choice, acid_conc, temp, time]])

# ให้ AI ทำนายผลผลิตน้ำตาลกูโคส (% Yield)
predicted_yield = model.predict(input_data)[0]

# แสดงกล่องผลลัพธ์ขนาดใหญ่
st.success(f"## *Predicted Glucose Yield: {predicted_yield:.2f} %*")

# 5. การวิเคราะห์ตามหลักเคมีสีเขียว (Green Chemistry Metrics)
st.write("---")
st.write("### 🍃 การวิเคราะห์เชิงสิ่งแวดล้อม")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="ระดับความเป็นมิตรต่อสิ่งแวดล้อม", value="สูง (Eco-friendly)" if acid_choice == 1 else "ต่ำ (Hazardous)")

with col2:
    # คำนวณความเสี่ยงของเสียแบบจำลอง
    waste_index = (acid_conc * time) / 100 if acid_choice == 2 else (acid_conc * time) / 500
    st.metric(label="ดัชนีของเสียตกค้าง (Waste Index)", value=f"{waste_index:.2f}")

if acid_choice == 1:
    st.info("💡 *คำแนะนำ:* การเลือกใช้กรดอินทรีย์ช่วยลดการกัดกร่อนของเครื่องจักรในโรงงาน และน้ำเสียสามารถบำบัดทางชีวภาพได้ง่าย เหมาะกับอุตสาหกรรมสีเขียวยุคใหม่")
else:
    st.warning("⚠️ *ข้อควรระวัง:* กรดอนินทรีย์ (กรดแก่) แม้จะให้ Yield ที่สูงกว่า แต่นำมาซึ่งค่าใช้จ่ายในการบำบัดสารพิษ ไอระเหยมีความเป็นกรดสูง และกัดกร่อนอุปกรณ์ในระบบอย่างรุนแรง")
