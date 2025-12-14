from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import uvicorn

# 1. Inisialisasi Aplikasi
app = FastAPI()

# 2. Pengaturan CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load Model AI
model = joblib.load("model/fire_prediction_model.pkl")

# 4. Definisikan Format Data Input
# HARUS DIUPDATE: Tambahkan wind_speed di sini
class FireInput(BaseModel):
    temperature: float
    humidity: float
    rainfall: float
    wind_speed: float  # <--- 1. TAMBAHKAN BARIS INI (Tipe datanya float)
    is_peatland: int   # 1 = Ya, 0 = Tidak

# 5. Endpoint Utama
@app.get("/")
def read_root():
    return {"status": "Server is running", "message": "Forest Fire Prediction API"}

# 6. Endpoint Prediksi
@app.post("/predict")
def predict_fire(data: FireInput):
    # Ambil data dari input user
    # PENTING: Urutan di dalam list ini WAJIB SAMA PERSIS dengan compare_models.py
    # Urutan Training: Temp, Humidity, Rainfall, Wind Speed, Is Peatland
    
    features = [[
        data.temperature, 
        data.humidity, 
        data.rainfall, 
        data.wind_speed,  # <--- 2. MASUKKAN VARIABELNYA DI SINI (Di tengah-tengah)
        data.is_peatland
    ]]
    
    # Prediksi (0 atau 1)
    prediction = model.predict(features)[0]
    
    # Hitung probabilitas
    probability = model.predict_proba(features)[0][1]
    
    # Terjemahkan hasil
    result_text = "BERBAHAYA: Potensi Kebakaran Tinggi" if prediction == 1 else "AMAN: Risiko Rendah"
    
    return {
        "prediction": int(prediction),
        "probability": f"{probability * 100:.1f}%",
        "result_text": result_text,
        "input_data": data
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)