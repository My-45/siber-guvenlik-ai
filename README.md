# 🔍 AI Destekli Anomali Tespit Sistemi
 Bu proje,  makine öğrenmesi kullanarak kredi kartı dolandırıcılığını 
otomatik olarak tespit etmektedir.

# HAZIRLAYAN: MERVE YILMAZ

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

### Neden Recall Düşük?

Bu projede **unsupervised (etiketsiz) öğrenme** tercih edilmiştir.
Model, hangi işlemin dolandırıcılık olduğunu önceden bilmeden
sadece "bu işlem diğerlerinden farklı mı?" sorusunu yanıtlar.

Recall'ın düşük olmasının üç temel nedeni vardır:

1. **Veri dengesizliği:** 284.807 işlemin yalnızca 492'si (%0.17)
dolandırıcılık. Model büyük çoğunluğu normal gördüğü için
anormal örüntüleri kaçırabiliyor.

2. **Etiket görmeden öğrenme:** Model "bu dolandırıcılık"
diye öğretilmediği için bazı dolandırıcılık işlemlerini
normal işlemlerle karıştırıyor. Supervised bir model
(%90+ recall) çok daha başarılı olurdu.

3. **Adversarial problem:** Gerçek dolandırıcılar normal
görünmeye çalışır — bu yüzden bazı işlemler modeli atlatıyor.

### Neden Yine de Unsupervised Seçtik?

Çünkü gerçek hayatta her saldırı tipi önceden bilinmiyor.
Yeni bir dolandırıcılık yöntemi çıktığında supervised model
onu tanıyamaz — unsupervised model ise yine de
"bu farklı görünüyor" diyebilir ve bu şekilde dolandırıcılık yöntemini tespit edebilir.


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

