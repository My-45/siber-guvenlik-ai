import streamlit as st
import pandas as pd
import pickle
import numpy as np
from groq import Groq

# Modeli yükle
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

import os
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🔍 AI Destekli Anomali Tespit Sistemi")
st.write("Kredi kartı işlemlerinde dolandırıcılık tespiti")

# Dosya yükleme
uploaded_file = st.file_uploader("CSV dosyası yükle", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(f"**{len(df)} işlem yüklendi.**")

    features = [col for col in df.columns if col != "Class"]
    X = df[features]
    X_scaled = scaler.transform(X)

    # Tahmin
    df["anomali"] = model.predict(X_scaled)
    df["anomali"] = df["anomali"].apply(lambda x: 1 if x == -1 else 0)

    anormal = df[df["anomali"] == 1]
    normal = df[df["anomali"] == 0]

    # Özet
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam İşlem", len(df))
    col2.metric("🚨 Şüpheli", len(anormal))
    col3.metric("✅ Normal", len(normal))

    st.subheader("🚨 Şüpheli İşlemler")
    st.dataframe(anormal.head(10))

    # LLM analizi
    st.subheader("🤖 AI Açıklaması")
    st.write("Bir işlem seç, AI ne tür saldırı olduğunu açıklasın:")

    secilen_index = st.selectbox(
        "Analiz edilecek işlem:",
        anormal.index[:10] if len(anormal) > 0 else []
    )

    if st.button("Analiz Et") and len(anormal) > 0:
        islem = df.loc[secilen_index, features].to_dict()
        islem_str = ", ".join([f"{k}: {round(v, 3)}" for k, v in list(islem.items())[:8]])

        with st.spinner("AI analiz ediyor..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{
                    "role": "user",
                    "content": f"""Sen bir siber güvenlik uzmanısın. 
Aşağıdaki kredi kartı işlemi bir AI tarafından ANOMALİ olarak işaretlendi.

İşlem verileri: {islem_str}

Kısa ve net Türkçe olarak şunları açıkla:
1. Bu işlem neden şüpheli görünüyor?
2. Hangi tür dolandırıcılık yöntemi olabilir?
3. Ne yapılmalı?"""
                }]
            )

        analiz = response.choices[0].message.content
        st.success("✅ AI Analizi Tamamlandı")
        st.write(analiz)