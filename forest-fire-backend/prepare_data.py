import pandas as pd
import numpy as np
import random
import os

# --- KONFIGURASI FINAL ---
DATA_COUNT = 5000   # Jumlah data banyak agar AI pintar
NOISE_LEVEL = 0.05  # Noise sedikit (5%) agar akurasi tinggi (85-95%)

# Lokasi Indonesia (Gambut & Mineral)
locations = [
    ["Gambut - Riau (Sumatera)", 0.5071, 101.4478, 1],
    ["Hutan Lindung - Jambi (Sumatera)", -1.6101, 103.6131, 0],
    ["Gambut - Palangkaraya (Kalimantan)", -2.2170, 113.9160, 1],
    ["Hutan Kutai - Kartanegara (Kalimantan)", -0.4437, 117.1566, 0],
    ["Ogan Komering Ilir (Sumatera Selatan)", -3.3970, 104.8310, 1]
]

# 1. LOAD DATA DISTRIBUSI ASLI (PORTUGAL)
# Kita butuh pola suhunya, lembabnya, dan HUJANNYA.
file_path = 'forestfires.csv' # Pastikan file ada di folder backend
if not os.path.exists(file_path):
    # Cek folder raw_data jika user memindahkannya
    file_path = 'raw_data/forestfires.csv'

try:
    df_org = pd.read_csv(file_path)
    print(f"Berhasil membaca pola dari {file_path} ({len(df_org)} data asli).")
    
    # Ambil array nilai asli
    real_temps = df_org['temp'].values
    real_rh = df_org['RH'].values
    real_rain = df_org['rain'].values # <--- INI KUNCINYA (Pola Hujan Asli)
    
except Exception as e:
    print(f"Error: {e}")
    print("Pastikan file forestfires.csv ada di folder backend!")
    exit()

new_data = []

print(f"Sedang meng-generate {DATA_COUNT} data sintetis berbasis distribusi asli...")

for i in range(DATA_COUNT):
    loc = random.choice(locations)
    
    # --- 2. SAMPLING DATA ASLI (Bukan Random Asal) ---
    # Kita comot satu angka dari data asli secara acak
    base_temp = random.choice(real_temps)
    base_rh = random.choice(real_rh)
    base_rain = random.choice(real_rain) # Mengambil pola hujan yang banyak 0-nya
    
    # --- 3. ADAPTASI KE INDONESIA ---
    # Suhu Indonesia lebih panas (+8 derajat rata-rata)
    temp = base_temp + 8.0 + np.random.normal(0, 1) 
    humidity = base_rh + np.random.normal(0, 2)
    
    # Hujan di Tropis biasanya lebih intensitasnya lebih tinggi sedikit
    # Tapi frekuensinya tetap mengikuti pola asli (banyak yang 0)
    rain = base_rain * 1.5 

    # Batasan Fisika Wajar (Cleaning)
    if temp < 24: temp = 24 + random.random()
    if temp > 40: temp = 40
    if humidity < 30: humidity = 30
    if humidity > 100: humidity = 100
    if rain < 0: rain = 0

    # --- 4. HITUNG RISIKO (Logic Probabilitas V2 - Lebih Halus) ---
    
    # Faktor Suhu (Linear): Panas = Bahaya
    # Suhu 24 -> 0, Suhu 40 -> 1.0
    prob_temp = (temp - 24) / 16
    if prob_temp < 0: prob_temp = 0
    
    # Faktor Lembab (Linear Terbalik): Kering = Bahaya
    prob_humid = (100 - humidity) / 100
    
    # Faktor Gambut (Konstan)
    prob_peat = 0.35 if loc[3] == 1 else 0.0
    
    # --- UPGRADE: Faktor Hujan (Logarithmic Decay) ---
    # Kita pakai Logaritma supaya penurunannya wajar.
    # Hujan dikit ngaruh dikit, hujan banyak ngaruh banyak.
    # np.log1p(x) adalah ln(1+x).
    # Contoh efek pengurang risiko:
    # Hujan 0.0mm -> Pengurang 0.0
    # Hujan 0.5mm -> Pengurang 0.12 (Kecil, api masih bisa hidup)
    # Hujan 5.0mm -> Pengurang 0.53 (Signifikan)
    # Hujan 15.0mm -> Pengurang 0.80 (Sangat Aman)
    prob_rain = -(np.log1p(rain) * 0.3) 
    
    # Total Probabilitas
    # Rumus: (Suhu 40%) + (Lembab 30%) + (Gambut) - (Hujan)
    total_prob = (prob_temp * 0.4) + (prob_humid * 0.3) + prob_peat + prob_rain
    
    # Tambah Noise Sedikit (Faktor X)
    noise = np.random.normal(0, NOISE_LEVEL) 
    final_prob = total_prob + noise
    
    # Cleaning batas probabilitas (0 sampai 1)
    if final_prob < 0: final_prob = 0
    if final_prob > 1: final_prob = 1
    
    # Tentukan Nasib (Threshold)
    # Kita naikkan sedikit thresholdnya ke 0.65 biar tidak terlalu sensitif
    fire_occurred = 1 if final_prob > 0.65 else 0
    
    new_data.append({
        'latitude': loc[1],
        'longitude': loc[2],
        'location_name': loc[0],
        'temperature': round(temp, 2),
        'humidity': int(humidity),
        'rainfall': round(rain, 2),
        'is_peatland': loc[3],
        'fire_occurred': fire_occurred
    })

# Simpan ke CSV
df = pd.DataFrame(new_data)
ratio = df['fire_occurred'].sum() / len(df) * 100
print(f"Selesai! Ratio Kebakaran: {ratio:.2f}%")

if not os.path.exists('dataset'): os.makedirs('dataset')
df.to_csv('dataset/indonesia_fire_data.csv', index=False)
print("File tersimpan: dataset/indonesia_fire_data.csv")