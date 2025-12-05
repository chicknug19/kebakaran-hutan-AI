import pandas as pd
import os

# 1. Definisikan Data Dummy
data = {
    'latitude': [-0.9492, -0.9550, -2.2170, -2.2200, -2.2250, 3.5952, 3.6000, -1.2692, -1.2700, -3.3194, -3.3200, 0.5071, 0.5100, 0.5150, -4.0000, -4.0050],
    'longitude': [100.3543, 100.3600, 113.9160, 113.9200, 113.9250, 98.6722, 98.6750, 116.8253, 116.8300, 114.5908, 114.6000, 101.4478, 101.4500, 101.4550, 104.0000, 104.0050],
    'location_name': ['Sumatra_Padang', 'Sumatra_Padang', 'Kalimantan_Tengah', 'Kalimantan_Tengah', 'Kalimantan_Tengah', 'Sumatra_Medan', 'Sumatra_Medan', 'Kalimantan_Balikpapan', 'Kalimantan_Balikpapan', 'Kalimantan_Banjarmasin', 'Kalimantan_Banjarmasin', 'Sumatra_Riau', 'Sumatra_Riau', 'Sumatra_Riau', 'Sumatra_Selatan', 'Sumatra_Selatan'],
    'temperature': [34.5, 28.0, 36.2, 35.5, 29.0, 33.0, 27.5, 35.8, 30.1, 37.0, 28.5, 36.5, 35.0, 29.0, 34.0, 27.0],
    'humidity': [45, 85, 30, 35, 80, 50, 90, 38, 75, 25, 82, 33, 40, 88, 42, 85],
    'rainfall': [0.0, 12.5, 0.0, 0.0, 5.0, 0.0, 20.0, 0.0, 2.0, 0.0, 10.0, 0.0, 0.0, 15.0, 0.0, 25.0],
    'is_peatland': [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    'fire_occurred': [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0]
}

# 2. Buat DataFrame
df = pd.DataFrame(data)

# 3. Cek apakah folder 'dataset' sudah ada, jika belum buat baru
if not os.path.exists('dataset'):
    os.makedirs('dataset')

# 4. Simpan ke CSV
csv_path = 'dataset/indonesia_fire_data.csv'
df.to_csv(csv_path, index=False)

print(f"Berhasil! File CSV telah dibuat di: {csv_path}")