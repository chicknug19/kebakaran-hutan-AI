import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load Dataset (Pastikan ini dataset yang SUDAH ada Wind Speed-nya)
df = pd.read_csv('dataset/indonesia_fire_data.csv')

# 2. Tentukan Fitur (X) dan Target (y)
# PENTING: Urutan di sini harus SAMA PERSIS dengan di main.py dan App.jsx
# Urutan: Suhu, Kelembaban, Curah Hujan, Kecepatan Angin, Lahan Gambut
features = ['temperature', 'humidity', 'rainfall', 'wind_speed', 'is_peatland']
X = df[features]
y = df['fire_occurred']

# 3. Bagi Data (80% Training, 20% Testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)

# 4. Buat Model Random Forest
# Kita gunakan n_estimators=300 agar lebih stabil (sesuai riset compare_models)
model = RandomForestClassifier(n_estimators=300, random_state=42)

# 5. Latih Model
print("Sedang melatih model Random Forest...")
model.fit(X_train, y_train)

# 6. Evaluasi Sebentar (Cek Akurasi)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Berhasil Dilatih!")
print(f"Akurasi Final: {accuracy * 100:.2f}%")
print("\nLaporan Detail:")
print(classification_report(y_test, y_pred))

# 7. Simpan Model ke File .pkl
# File ini yang nanti dipanggil oleh main.py
joblib.dump(model, 'model/fire_prediction_model.pkl')
print("Model tersimpan sebagai 'model/fire_prediction_model.pkl'")