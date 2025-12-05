import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet';

// Fix icon marker default Leaflet di React
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// --- KONFIGURASI API KEY ---
const API_KEY = "4a8c9467d6143abeff23d67482dc0855" 

// --- DATA LOKASI ---
const MONITORING_STATIONS = [
  { id: 1, name: "Gambut - Riau (Sumatera)", lat: 0.5071, lon: 101.4478, defaultPeat: 1 },
  { id: 2, name: "Hutan Lindung - Jambi (Sumatera)", lat: -1.6101, lon: 103.6131, defaultPeat: 0 },
  { id: 3, name: "Gambut - Palangkaraya (Kalimantan)", lat: -2.2170, lon: 113.9160, defaultPeat: 1 },
  { id: 4, name: "Hutan Kutai - Kartanegara (Kalimantan)", lat: -0.4437, lon: 117.1566, defaultPeat: 0 },
  { id: 5, name: "Ogan Komering Ilir (Sumatera Selatan)", lat: -3.3970, lon: 104.8310, defaultPeat: 1 },
  
  // --- SKENARIO DEMO BARU (Tanpa Koordinat) ---
  // Lat/Lon kita set null agar peta tidak bergerak
  { id: 99, name: "⚠️ SKENARIO DEMO: Cuaca Ekstrem (Kebakaran)", lat: null, lon: null, defaultPeat: 1 },
]

// Komponen untuk animasi geser peta
function MapUpdater({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center) { // Hanya gerak jika ada koordinat valid
        map.flyTo(center, 10);
    }
  }, [center, map]);
  return null;
}

function App() {
  const [formData, setFormData] = useState({
    temperature: "",
    humidity: "",
    rainfall: "",
    is_peatland: 0
  })

  const [selectedStation, setSelectedStation] = useState("") 
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [weatherStatus, setWeatherStatus] = useState("")
  
  // Default Map Center (Indonesia Tengah)
  const [mapCenter, setMapCenter] = useState([-0.7893, 113.9213]) 

  const handleLocationChange = async (e) => {
    const stationId = parseInt(e.target.value)
    
    if (!stationId) {
      setSelectedStation("")
      return
    }

    const station = MONITORING_STATIONS.find(s => s.id === stationId)
    setSelectedStation(stationId)
    
    // --- LOGIKA SKENARIO DEMO ---
    if (station.id === 99) {
        // 1. Jangan geser peta (mapCenter tetap yang lama)
        // 2. Set Status Demo
        setWeatherStatus("⚠️ Mode Simulasi: Memaksa kondisi sangat kering & panas...");
        
        // 3. Paksa Data Form (Manual Override)
        setFormData({
            temperature: 39.5,  // Sangat Panas
            humidity: 20,       // Sangat Kering
            rainfall: 0,        // Tidak Hujan
            is_peatland: 1      // Lahan Gambut
        })
        return; // BERHENTI DI SINI (Jangan panggil API Cuaca)
    }

    // --- LOGIKA NORMAL (Panggil API) ---
    // Update Posisi Peta
    setMapCenter([station.lat, station.lon])
    
    setWeatherStatus(`Mengambil data satelit...`)
    setFormData(prev => ({ ...prev, is_peatland: station.defaultPeat }))

    try {
      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?lat=${station.lat}&lon=${station.lon}&appid=${API_KEY}&units=metric`
      )
      
      const data = await response.json()

      if (response.ok) {
        let rainValue = data.rain ? data.rain['1h'] : 0;
        
        setFormData(prev => ({
          ...prev,
          temperature: data.main.temp,
          humidity: data.main.humidity,
          rainfall: rainValue
        }))
        setWeatherStatus(`✅ Data Terkini: ${data.weather[0].description} (Updated: ${new Date().toLocaleTimeString()})`)
      } else {
        setWeatherStatus("❌ Gagal mengambil data cuaca.")
      }
    } catch (error) {
      console.error(error)
      setWeatherStatus("❌ Error koneksi ke satelit.")
    }
  }

  const handleChange = (e) => setFormData({...formData, [e.target.name]: e.target.value})

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          temperature: parseFloat(formData.temperature),
          humidity: parseFloat(formData.humidity),
          rainfall: parseFloat(formData.rainfall),
          is_peatland: parseInt(formData.is_peatland)
        }),
      })
      const data = await response.json()
      setResult(data)
    } catch (error) {
      alert("Backend Python belum nyala!")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex flex-col md:flex-row bg-fire-animated overflow-hidden">
      
      {/* --- BAGIAN KIRI: PETA --- */}
      <div className="w-full md:w-3/5 h-1/2 md:h-full relative z-0">
        <MapContainer center={mapCenter} zoom={5} style={{ height: "100%", width: "100%" }}>
          <TileLayer
            url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            attribution='&copy; Esri'
          />
          
          <MapUpdater center={mapCenter} />

          {/* Marker Lokasi (Hanya render jika punya koordinat) */}
          {MONITORING_STATIONS.map(station => (
            station.lat && station.lon ? (
                <Marker key={station.id} position={[station.lat, station.lon]}>
                <Popup>{station.name}</Popup>
                </Marker>
            ) : null
          ))}
        </MapContainer>
        
        <div className="absolute top-4 right-4 z-[400] bg-white/80 backdrop-blur px-4 py-2 rounded-lg shadow-lg">
           <h2 className="font-bold text-gray-800">🌏 FireWatch Satellite Map</h2>
           <p className="text-xs text-gray-600">Pantauan visual area hutan</p>
        </div>
      </div>

      {/* --- BAGIAN KANAN: FORMULIR --- */}
      <div className="w-full md:w-2/5 h-1/2 md:h-full flex items-center justify-center p-6 relative z-10 overflow-y-auto">
        <div className="bg-white/90 backdrop-blur-md p-6 rounded-xl shadow-2xl w-full max-w-md border border-white/20">
          
          <h1 className="text-2xl font-bold text-center text-gray-800 mb-1">🔥 FireWatch AI</h1>
          <p className="text-center text-gray-500 mb-4 text-xs">Sistem Analisa Risiko Kebakaran</p>

          <div className="mb-4 bg-blue-50 p-3 rounded-lg border border-blue-200">
              <label className="block text-xs font-bold text-gray-700 mb-1">📍 Pilih Lokasi / Skenario</label>
              <select 
                value={selectedStation} 
                onChange={handleLocationChange}
                className="w-full p-2 text-sm border border-blue-300 rounded-md focus:ring-2 focus:ring-blue-500 outline-none bg-white"
              >
                <option value="">-- Pilih Hutan Indonesia --</option>
                {MONITORING_STATIONS.map(station => (
                  <option key={station.id} value={station.id} className={station.id === 99 ? "font-bold text-red-600" : ""}>
                    {station.name}
                  </option>
                ))}
              </select>
              {weatherStatus && <p className={`text-[10px] mt-1 font-semibold ${weatherStatus.includes("Mode Simulasi") ? "text-red-600" : "text-green-700"}`}>{weatherStatus}</p>}
          </div>

          <form onSubmit={handleSubmit} className="space-y-3">
            <div className='grid grid-cols-2 gap-3'>
              <div>
                <label className="block text-xs font-medium text-gray-500">Suhu (°C)</label>
                <input type="number" name="temperature" value={formData.temperature} readOnly className="mt-1 w-full p-2 border rounded bg-gray-100 font-bold" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-500">Kelembaban (%)</label>
                <input type="number" name="humidity" value={formData.humidity} readOnly className="mt-1 w-full p-2 border rounded bg-gray-100 font-bold" />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-500">Curah Hujan (mm)</label>
              <input type="number" name="rainfall" value={formData.rainfall} readOnly className="mt-1 w-full p-2 border rounded bg-gray-100 font-bold" />
            </div>
            
            {/* --- JENIS LAHAN (OTOMATIS TERKUNCI) --- */}
            <div>
              <label className="block text-xs font-medium text-gray-500">Jenis Lahan (Geologis)</label>
              <div className="relative">
                <input 
                  type="text" 
                  value={formData.is_peatland === 1 ? "⚠️ Lahan Gambut (Sangat Rawan)" : "✅ Tanah Mineral (Stabil)"} 
                  readOnly 
                  className={`mt-1 w-full p-2 border rounded-md font-bold text-sm ${
                    formData.is_peatland === 1 
                      ? "bg-red-50 text-red-800 border-red-200" 
                      : "bg-green-50 text-green-800 border-green-200"
                  }`} 
                />
                <span className="absolute right-3 top-3 text-xs">🔒</span>
              </div>
              <p className="text-[10px] text-gray-400 mt-1">
                *Jenis lahan ditentukan otomatis berdasarkan data geologis.
              </p>
            </div>

            <button type="submit" disabled={!selectedStation || loading} className="w-full bg-orange-600 text-white py-2 rounded-md font-bold hover:bg-orange-700 transition shadow-md">
              {loading ? "Menganalisa..." : "ANALISA RISIKO"}
            </button>
          </form>

          {result && (
            <div className={`mt-4 p-3 rounded-lg text-center border-2 animate-pulse ${result.prediction === 1 ? "bg-red-50 border-red-500 text-red-700" : "bg-green-50 border-green-500 text-green-700"}`}>
              <h2 className="text-lg font-extrabold">{result.result_text}</h2>
              <p className="text-xs">Probabilitas: {result.probability}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App