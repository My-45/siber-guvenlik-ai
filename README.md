# 🔍 AI Destekli Anomali Tespit Sistemi
 Bu proje,  makine öğrenmesi kullanarak kredi kartı dolandırıcılığını 
otomatik olarak tespit etmektedir.

## 📌 Proje Hakkında

Gerçek bir Avrupa bankasına ait 284.807 kredi kartı işlemi 
üzerinde çalışan bu sistem:
- **IsolationForest** algoritmasıyla anomali tespiti yapar
- **Groq LLM** ile şüpheli işlemleri Türkçe açıklar
- **Streamlit** ile interaktif web arayüzü sunar

## 🎯 Sonuçlar

| Algoritma | Recall | Precision | F1 |
|-----------|--------|-----------|-----|
| IsolationForest (c=0.002) | %28 | %24 | %26 |


## 🛠️ Kullanılan Teknolojiler

- Python 3.13
- Scikit-learn (IsolationForest, StandardScaler)
- Streamlit
- Groq API (LLaMA3)
- Pandas, Matplotlib

## 📂 Kurulum

1. Repoyu klonla: git clone https://github.com/My-45/siber-guvenlik-ai.git
2. Sanal ortam oluştur:python -m venv venv
venv\Scripts\activate
3. Kütüphaneleri kur:pip install pandas scikit-learn streamlit matplotlib groq python-dotenv
4.  Veri setini indir:
[Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
→ `creditcard.csv` dosyasını proje klasörüne taşı

5. `.env` dosyası oluştur:GROQ_API_KEY=senin_api_keyin
6.  Modeli eğit: py model.py
7.  Uygulamayı başlat: streamlit run app.py
   ## 🔍 Nasıl Çalışır?

1. `creditcard.csv` dosyasını arayüzden yükle
2. Model otomatik analiz eder
3. Şüpheli işlemleri listeler
4. "Analiz Et" butonuyla LLM açıklaması al

## ⚠️ Önemli Not

Veri seti gizlilik nedeniyle repoya dahil edilmemiştir.
Kaggle'dan indirmeniz gerekmektedir.

