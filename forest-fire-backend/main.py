from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import uvicorn

# 1. Inisialisasi Aplikasi
app = FastAPI()

# 2. Pengaturan CORS (Agar bisa diakses oleh React JS)
origins = [
    "http://localhost:3000",  # Port standar React
    "http://localhost:5173",  # Port standar Vite (jika pakai Vite)
    "*"                       # Izinkan semua (opsional untuk development)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load Model AI
# Pastikan nama file sama dengan yang ada di folder model/
model = joblib.load("model/fire_prediction_model.pkl")

# 4. Definisikan Format Data Input
# Harus sama urutannya dengan saat training (Suhu, Lembab, Hujan, Gambut)
class FireInput(BaseModel):
    temperature: float
    humidity: float
    rainfall: float
    is_peatland: int  # 1 = Ya, 0 = Tidak

# 5. Endpoint Utama (Cek Server Nyala)
@app.get("/")
def read_root():
    return {"status": "Server is running", "message": "Forest Fire Prediction API"}

# 6. Endpoint Prediksi (Ini yang dipanggil React)
@app.post("/predict")
def predict_fire(data: FireInput):
    # Ambil data dari input user
    features = [[data.temperature, data.humidity, data.rainfall, data.is_peatland]]
    
    # Prediksi (0 atau 1)
    prediction = model.predict(features)[0]
    
    # Hitung probabilitas/kemungkinan (misal: 0.85 artinya 85% yakin)
    probability = model.predict_proba(features)[0][1]
    
    # Terjemahkan hasil ke bahasa manusia
    result_text = "BERBAHAYA: Potensi Kebakaran Tinggi" if prediction == 1 else "AMAN: Risiko Rendah"
    
    return {
        "prediction": int(prediction),
        "probability": f"{probability * 100:.1f}%",
        "result_text": result_text,
        "input_data": data
    }

# Kode di bawah ini agar bisa dijalankan langsung dengan 'python main.py'
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)