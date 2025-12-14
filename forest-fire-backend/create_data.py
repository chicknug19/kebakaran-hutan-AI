import pandas as pd
import numpy as np
import random

# Jumlah data
NUM_SAMPLES = 5000

LOCATIONS = [
    {"name": "Hutan Lindung - Jambi (Sumatera)", "lat": -1.6101, "lon": 103.6131, "is_peatland": 0},
    {"name": "Gambut - Riau (Sumatera)", "lat": 0.5071, "lon": 101.4478, "is_peatland": 1},
    {"name": "Ogan Komering Ilir (Sumatera Selatan)", "lat": -3.3970, "lon": 104.8310, "is_peatland": 1},
    {"name": "Hutan Kutai - Kartanegara (Kalimantan)", "lat": -0.4437, "lon": 117.1566, "is_peatland": 0},
    {"name": "Gambut - Palangkaraya (Kalimantan)", "lat": -2.2170, "lon": 113.9160, "is_peatland": 1}
]

data = []

print("Generate Data: Advanced (With Wind Speed)...")

for _ in range(NUM_SAMPLES):
    loc = random.choice(LOCATIONS)
    
    # KITA BAGI JADI 3 TIPE CUACA UTAMA
    weather_type = random.choices(
        ['BADAI_HUJAN', 'NORMAL', 'EKSTRIM_KERING'], 
        weights=[25, 45, 30] 
    )[0]
    
    # Default values
    fire_occurred = 0
    
    if weather_type == 'BADAI_HUJAN':
        # Hujan + Angin Kencang = Tetap Aman (Air memadamkan api)
        temperature = round(random.uniform(20, 27), 2)
        humidity = random.randint(80, 99)
        rainfall = round(random.uniform(10.0, 60.0), 1) 
        wind_speed = round(random.uniform(5.0, 20.0), 2) # Angin kencang
        fire_occurred = 0 
        
    elif weather_type == 'NORMAL':
        # Cuaca biasa, bisa gerimis, bisa mendung
        temperature = round(random.uniform(27, 32), 2)
        humidity = random.randint(55, 80)
        rainfall = round(random.uniform(0.0, 5.0), 1) # Gerimis/Kering
        wind_speed = round(random.uniform(1.0, 10.0), 2) # Angin sepoi-sepoi
        
        # Peluang kebakaran sangat kecil (kecuali human error di gambut)
        chance = 2
        if loc['is_peatland'] == 1 and rainfall < 1.0:
            chance += 10
            
        if random.randint(0, 100) < chance:
            fire_occurred = 1
        else:
            fire_occurred = 0
            
    else: # EKSTRIM_KERING
        # Panas + Kering + (Mungkin) Angin Kencang
        temperature = round(random.uniform(33, 41), 2)
        humidity = random.randint(20, 50)
        rainfall = 0.0
        wind_speed = round(random.uniform(3.0, 18.0), 2) # Angin bervariasi
        
        # LOGIKA SCORING BAHAYA
        danger_score = 0
        
        # 1. Faktor Suhu & Lembab
        if temperature > 35: danger_score += 30
        if humidity < 40: danger_score += 20
        
        # 2. Faktor Lahan Gambut
        if loc['is_peatland'] == 1:
            danger_score += 25
            
        # 3. FAKTOR BARU: ANGIN
        # Angin kencang menyuplai oksigen ke api
        if wind_speed > 10.0: 
            danger_score += 15
        elif wind_speed > 15.0:
            danger_score += 25
        
        # Base probability 10%
        total_chance = 10 + danger_score
        
        # Limit max chance 98%
        if total_chance > 98: total_chance = 98
        
        if random.randint(0, 100) < total_chance:
            fire_occurred = 1
        else:
            fire_occurred = 0

    data.append([
        loc['lat'], loc['lon'], loc['name'], 
        temperature, humidity, rainfall, wind_speed, # <-- Ada Wind Speed
        loc['is_peatland'], fire_occurred
    ])

# Simpan
cols = ['latitude', 'longitude', 'location_name', 'temperature', 'humidity', 'rainfall', 'wind_speed', 'is_peatland', 'fire_occurred']
df = pd.DataFrame(data, columns=cols)
df.to_csv("dataset/indonesia_fire_data.csv", index=False)

print(f"Dataset baru dengan Angin (Wind Speed) berhasil dibuat!")
print(df[['temperature', 'wind_speed', 'fire_occurred']].head())