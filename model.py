
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import pickle

print("Veri yükleniyor...")
df = pd.read_csv("creditcard.csv")

# Sadece orijinal sütunları kullan
features = [col for col in df.columns if col != "Class"]
X = df[features]

# Ölçeklendirme
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Modeli eğit
print("Model eğitiliyor...")
model = IsolationForest(
    n_estimators=100,
    contamination=0.002,
    random_state=42
)
model.fit(X_scaled)

# Kaydet
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Model kaydedildi!")

# Sonuçlar
df["tahmin"] = model.predict(X_scaled)
df["anomali"] = df["tahmin"].apply(lambda x: 1 if x == -1 else 0)

gercek = df["Class"].sum()
bulunan = df[df["anomali"] == 1]["Class"].sum()
print(f"Gerçek dolandırıcılık: {gercek}")
print(f"Bulunan: {bulunan}")
print(f"Başarı: %{round(bulunan/gercek*100, 1)}")
print(classification_report(df["Class"], df["anomali"],
      target_names=["Normal", "Dolandırıcılık"]))

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, df["Class"], test_size=0.2, random_state=42
)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

print("\n--- Supervised (RandomForest) ---")
print(classification_report(y_test, y_pred,
      target_names=["Normal", "Dolandırıcılık"]))
