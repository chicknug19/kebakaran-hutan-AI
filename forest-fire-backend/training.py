# training.py (Updated)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Load Dataset
df = pd.read_csv("dataset/indonesia_fire_data.csv")

# 2. Pisahkan Fitur (X) dan Label (y)
# Kita pakai: Suhu, Kelembaban, Curah Hujan, Apakah Gambut
X = df[['temperature', 'humidity', 'rainfall', 'is_peatland']]
y = df['fire_occurred']

# 3. Bagi Data Training & Testing (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Latih Model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# 5. Cek Akurasi (Untuk Laporan)
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 6. Simpan Model
joblib.dump(clf, "model/fire_prediction_model.pkl")
print("Model berhasil disimpan!")