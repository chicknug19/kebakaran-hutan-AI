import pandas as pd
import numpy as np
import random

# Jumlah data total
NUM_SAMPLES = 5000

LOCATIONS = [
    {"name": "Hutan Lindung - Jambi (Sumatera)", "lat": -1.6101, "lon": 103.6131, "is_peatland": 0},
    {"name": "Gambut - Riau (Sumatera)", "lat": 0.5071, "lon": 101.4478, "is_peatland": 1},
    {"name": "Ogan Komering Ilir (Sumatera Selatan)", "lat": -3.3970, "lon": 104.8310, "is_peatland": 1},
    {"name": "Hutan Kutai - Kartanegara (Kalimantan)", "lat": -0.4437, "lon": 117.1566, "is_peatland": 0},
    {"name": "Gambut - Palangkaraya (Kalimantan)", "lat": -2.2170, "lon": 113.9160, "is_peatland": 1}
]

data = []

print("Generate Data: Realistis (Ada Hujan tapi Tetap Kebakaran)...")

for _ in range(NUM_SAMPLES):
    loc = random.choice(LOCATIONS)
    
    # Kita bagi cuaca menjadi 3 Tipe
    weather_type = random.choices(
        ['HUJAN_DERAS', 'GERIMIS', 'KERING'], 
        weights=[20, 30, 50] # 20% Hujan Deras, 30% Gerimis, 50% Kering
    )[0]
    
    # Default values
    fire_occurred = 0
    
    if weather_type == 'HUJAN_DERAS':
        # SKENARIO 1: Hujan Deras -> Api Mati Total
        temperature = round(random.uniform(20, 26), 2)
        humidity = random.randint(85, 99)
        rainfall = round(random.uniform(10.0, 50.0), 1) # Di atas 10mm
        fire_occurred = 0 # Mustahil kebakaran
        
    elif weather_type == 'GERIMIS':
        # SKENARIO 2: Gerimis -> INI YANG ANDA MINTA
        # Hujan ada, tapi dikit. Api masih bisa hidup (terutama di gambut).
        temperature = round(random.uniform(26, 31), 2)
        humidity = random.randint(60, 85)
        rainfall = round(random.uniform(0.1, 5.0), 1) # Hujan ringan
        
        # Logika: Kalau Gerimis + Gambut, peluang kebakaran TETAP ADA (kecil)
        chance = 5 # Peluang dasar 5%
        if loc['is_peatland'] == 1:
            chance += 15 # Di gambut, gerimis tidak mempan (peluang naik jadi 20%)
            
        if random.randint(0, 100) < chance:
            fire_occurred = 1
        else:
            fire_occurred = 0
            
    else: # weather_type == 'KERING'
        # SKENARIO 3: Tidak Hujan -> Risiko Tinggi
        rainfall = 0.0
        
        # Sub-skenario: Panas Normal vs Panas Ekstrim
        if random.random() < 0.6: # 60% hari kering itu panas biasa
            temperature = round(random.uniform(28, 33), 2)
            humidity = random.randint(45, 70)
            chance = 10 # Risiko rendah
        else: # 40% hari kering itu Panas Ekstrim (Heatwave)
            temperature = round(random.uniform(34, 40), 2)
            humidity = random.randint(20, 45)
            chance = 80 # Risiko SANGAT TINGGI
            
            # Faktor Gambut memperparah
            if loc['is_peatland'] == 1:
                chance += 15 # Jadi 95%
        
        # Eksekusi peluang kebakaran
        if random.randint(0, 100) < chance:
            fire_occurred = 1
        else:
            fire_occurred = 0

    data.append([
        loc['lat'], loc['lon'], loc['name'], 
        temperature, humidity, rainfall, 
        loc['is_peatland'], fire_occurred
    ])

# Simpan
df = pd.DataFrame(data, columns=['latitude', 'longitude', 'location_name', 'temperature', 'humidity', 'rainfall', 'is_peatland', 'fire_occurred'])
df.to_csv("dataset/indonesia_fire_data.csv", index=False)

print(f"Selesai! Data mencakup skenario 'Hujan Gerimis tapi Kebakaran'.")
print("Sebaran Data:")
print(df.groupby('is_peatland')['fire_occurred'].value_counts())