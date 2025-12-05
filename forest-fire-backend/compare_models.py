import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
# Import 3 Algoritma Berbeda
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import warnings

# Matikan warning merah yang tidak perlu (agar rapi)
warnings.filterwarnings('ignore')

print("="*40)
print("   MEMULAI KOMPETISI ALGORITMA AI")
print("="*40)

# 1. Load Data
try:
    df = pd.read_csv("dataset/indonesia_fire_data.csv")
    print(f"Dataset dimuat: {len(df)} baris data")
except:
    print("Error: File 'dataset/indonesia_fire_data.csv' tidak ditemukan.")
    exit()

X = df[['temperature', 'humidity', 'rainfall', 'is_peatland']]
y = df['fire_occurred']

# 2. Split Data (80% Latihan, 20% Ujian)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Definisikan Para Peserta (Model)
models = {
    "Logistic Regression": LogisticRegression(),
    "Support Vector Machine (SVM)": SVC(),
    "Random Forest (Juara Bertahan)": RandomForestClassifier(n_estimators=100)
}

results = []

print("\nSedang melatih model... (Mohon tunggu sebentar)\n")

# 4. Latih & Bandingkan
print(f"{'NAMA MODEL':<35} | {'AKURASI':<10}")
print("-" * 50)

for name, model in models.items():
    # Latih
    model.fit(X_train, y_train)
    
    # Uji
    y_pred = model.predict(X_test)
    
    # Nilai
    acc = accuracy_score(y_test, y_pred)
    results.append({"Model": name, "Akurasi": acc})
    
    print(f"{name:<35} | {acc*100:.2f}%")

print("-" * 50)

# Cari Pemenang
best_model = max(results, key=lambda x:x['Akurasi'])
print(f"\n🏆 PEMENANG: {best_model['Model']}")
print(f"   Skor Akhir: {best_model['Akurasi']*100:.2f}%")
print("="*50)