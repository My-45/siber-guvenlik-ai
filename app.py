import streamlit as st
import pandas as pd
import pickle
import numpy as np
import os
from groq import Groq
from dotenv import load_dotenv


# SAYFA AYARI

st.set_page_config(
    page_title="Yapay Zeka Anomali Tespit Sistemi",
    page_icon="🛡️",
    layout="wide"
)


st.markdown("""
<style>

/* Ana arka plan (beyaz temiz tasarım) */
.stApp {
    background-color: #f5f7fb;
}

/* Başlık kutusu */
.title-box {
    background: linear-gradient(135deg, #ffffff, #f1f5f9);
    border: 1px solid #e5e7eb;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

/* Başlık */
.title {
    font-size: 34px;
    font-weight: 900;
    color: #111827;
}

/* Alt yazı */
.subtitle {
    color: #6b7280;
    font-size: 14px;
}

/* Kartlar */
.card {
    background-color: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    transition: 0.25s;
}

/* Hover efekti */
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

/* metric */
.metric {
    font-size: 22px;
    font-weight: bold;
    color: #2563eb;
}

/* küçük yazı */
.small {
    color: #6b7280;
    font-size: 13px;
}

/* sidebar (soft pastel) */
[data-testid="stSidebar"] {
    background-color: #eef2ff;
}

</style>
""", unsafe_allow_html=True)


# BAŞLIK KISMI

st.markdown("""
<div class="title-box">
    <div class="title">🛡️ AI Destekli Anomali ve Dolandırıcılık Tespit Sistemi</div>
    <div class="subtitle">Gerçek zamanlı işlem analizi ve akıllı risk değerlendirmesi</div>
</div>
""", unsafe_allow_html=True)

# MODEL KISMI

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)


# API KISMI

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ======================
# SIDEBAR (SOFT PANEL)
# ======================
st.sidebar.title("⚙️ Kontrol Paneli")

gorunum = st.sidebar.selectbox(
    "Görünüm Seç",
    ["📊 Genel Durum", "🚨 Şüpheli İşlemler", "📂 Veri Seti"]
)

st.sidebar.markdown("---")
st.sidebar.info("AI tabanlı anomali tespit sistemi")

# ======================
# DOSYA YÜKLEME
# ======================
uploaded_file = st.file_uploader("📁 CSV Dosyası Yükle", type="csv")

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.success(f"✅ {len(df)} işlem yüklendi")

    features = [col for col in df.columns if col != "Class"]
    X = df[features]
    X_scaled = scaler.transform(X)

    df["anomali"] = model.predict(X_scaled)
    df["anomali"] = df["anomali"].apply(lambda x: 1 if x == -1 else 0)

    anormal = df[df["anomali"] == 1]
    normal = df[df["anomali"] == 0]

    risk = len(anormal) / len(df)

    # ======================
    # GENEL DURUM
    # ======================
    if gorunum == "📊 Genel Durum":

        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f"""
        <div class="card">
        <div class="small">Toplam İşlem</div>
        <div class="metric">{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="card">
        <div class="small">Şüpheli İşlem</div>
        <div class="metric">{len(anormal)}</div>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="card">
        <div class="small">Normal İşlem</div>
        <div class="metric">{len(normal)}</div>
        </div>
        """, unsafe_allow_html=True)

        col4.markdown(f"""
        <div class="card">
        <div class="small">Risk Oranı</div>
        <div class="metric">{risk*100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.subheader("📊 İşlem Dağılımı")

        chart = pd.DataFrame({
            "Kategori": ["Normal", "Şüpheli"],
            "Adet": [len(normal), len(anormal)]
        })

        st.bar_chart(chart.set_index("Kategori"))

        if risk > 0.3:
            st.error("🔴 Yüksek Risk")
        elif risk > 0.1:
            st.warning("🟠 Orta Risk")
        else:
            st.success("🟢 Düşük Risk")

    
    # ŞÜPHELİ İŞLEMLER
   
    elif gorunum == "🚨 Şüpheli İşlemler":

        st.subheader("🚨 Şüpheli İşlem Listesi")

        if len(anormal) == 0:
            st.success("Şüpheli işlem yok 🎉")
        else:

            for i, row in anormal.head(10).iterrows():
                with st.expander(f"🔎 İşlem ID: {i}"):
                    st.write(row)

            st.markdown("---")

            st.subheader("🤖 Yapay Zeka Analizi")

            secilen = st.selectbox("İşlem seç", anormal.index[:10])

            if st.button("Analiz Et"):

                islem = df.loc[secilen, features].to_dict()
                islem_str = ", ".join([f"{k}: {round(v, 3)}" for k, v in list(islem.items())[:8]])

                with st.spinner("Analiz yapılıyor..."):

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{
                            "role": "user",
                            "content": f"""
Sen bir siber güvenlik uzmanısın.

Bu işlem şüpheli:

{islem_str}

Türkçe açıkla:
- Neden şüpheli?
- Olası saldırı?
- Ne yapılmalı?
"""
                        }]
                    )

                analiz = response.choices[0].message.content

                st.success("Analiz tamamlandı")
                st.write(analiz)

    
    # VERİ KISMI
    elif gorunum == "📂 Veri Seti":

        st.subheader("📂 Veri Seti")

        st.dataframe(df, use_container_width=True)

        st.download_button(
            "📥 Sonucu İndir",
            df.to_csv(index=False),
            "sonuc.csv",
            "text/csv"
        )

else:
    st.info("⬆️ Analiz için CSV dosyası yükleyiniz")