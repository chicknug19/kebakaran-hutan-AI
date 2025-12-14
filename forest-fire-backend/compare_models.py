import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# --- IMPORT MODEL ---
from sklearn.linear_model import LogisticRegression 
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# --- 1. LOAD DATASET ---
df = pd.read_csv("dataset/indonesia_fire_data.csv") 

# --- 2. PERSIAPAN DATA ---
# Sesuaikan nama kolom dengan CSV Anda
X = df[['temperature', 'humidity', 'rainfall', 'wind_speed', 'is_peatland']]
y = df['fire_occurred'] 

# Split Data (80% Latih, 20% Uji)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scaling (Penting untuk SVM dan Logistic Regression)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- 3. DEFINISI MODEL ---
models = {
    "Logistic Regression": LogisticRegression(),
    "SVM (Support Vector Machine)": SVC(),
    "Random Forest": RandomForestClassifier(n_estimators=300, max_depth=15, random_state=42)
}

# --- 4. TRAINING & EVALUASI (OUTPUT PERSEN) ---
print("="*70)
print("HASIL PERBANDINGAN MODEL (FORMAT PERSEN)")
print("="*70)

for name, model in models.items():
    # Training
    if name == "Random Forest":
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    else:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    
    # Ambil report dalam bentuk Dictionary
    report = classification_report(y_test, y_pred, output_dict=True)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"MODEL: {name.upper()}")
    print(f"Total Akurasi: {acc*100:.2f}%")
    print("-" * 40)
    
    # KITA GANTI LABELNYA DI SINI
    
    # --- STATUS: BAHAYA KEBAKARAN (Dulunya Class 1) ---
    prec_fire = report['1']['precision'] * 100
    rec_fire  = report['1']['recall'] * 100
    f1_fire   = report['1']['f1-score'] * 100
    
    print(f"Status: BAHAYA KEBAKARAN (Api Terdeteksi)")
    print(f" > Seberapa Tepat Tebakannya (Precision) : {prec_fire:.2f}%")
    print(f" > Seberapa Banyak Api Terdeteksi (Recall): {rec_fire:.2f}%")
    print(f" > Nilai Kualitas Model (F1-Score)        : {f1_fire:.2f}%")
    
    print("-" * 40)
    
    # --- STATUS: AMAN (Dulunya Class 0) ---
    prec_safe = report['0']['precision'] * 100
    rec_safe  = report['0']['recall'] * 100
    f1_safe   = report['0']['f1-score'] * 100
    
    print(f"Status: KONDISI AMAN (Tidak Ada Api)")
    print(f" > Precision : {prec_safe:.2f}%")
    print(f" > Recall    : {rec_safe:.2f}%")
    print(f" > F1-Score  : {f1_safe:.2f}%")
    
    print("="*70)