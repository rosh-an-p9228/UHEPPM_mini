import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [locationData, setLocationData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      console.log('Fetching data from backend...')
      const response = await axios.get('http://127.0.0.1:8000/api/dashboard/?location_id=nerul')
      console.log('Response received:', response.data)
      setLocationData(response.data)
      setLoading(false)
    } catch (err) {
      console.error('Error fetching data:', err)
      setError(`Failed to connect: ${err.message}. Make sure the API is running at http://127.0.0.1:8000`)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#080c14] text-slate-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl font-bold mb-4">UrbanHeat AI</div>
          <div className="text-slate-400">Loading climate intelligence...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#080c14] text-slate-100 flex items-center justify-center p-4">
        <div className="text-center max-w-md">
          <div className="text-2xl font-bold mb-4 text-red-400">Connection Error</div>
          <div className="text-slate-400 mb-6">{error}</div>
          <button 
            onClick={fetchDashboardData}
            className="px-6 py-3 bg-orange-500 hover:bg-orange-600 rounded-lg font-semibold"
          >
            Retry Connection
          </button>
        </div>
      </div>
    )
  }

  const kpi = locationData?.kpi || {}
  const weather = locationData?.weather || {}
  const satellite = locationData?.satellite || {}
  const vegetation = locationData?.vegetation || {}
  const traffic = locationData?.traffic || {}
  const airQuality = locationData?.air_quality || {}
  const population = locationData?.population || {}
  const location = locationData?.location || {}

  return (
    <div className="min-h-screen bg-[#080c14] text-slate-100 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl sm:text-5xl font-extrabold">
            <span className="text-slate-100">Urban</span>
            <span className="bg-gradient-to-r from-orange-400 via-amber-300 to-cyan-300 bg-clip-text text-transparent">Heat AI</span>
          </h1>
          <p className="text-slate-400 text-sm sm:text-base">Urban Heat Entrapment Prediction and Prevention Model</p>
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900/90 border border-slate-700 text-xs font-mono">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            <span>Live Climate Intelligence</span>
          </div>
        </div>

        {/* Debug Info */}
        <div className="p-4 rounded-lg bg-slate-800 border border-slate-700 text-xs font-mono">
          <div>Backend Status: {locationData ? '✅ Connected' : '❌ Not Connected'}</div>
          <div>Data Keys: {locationData ? Object.keys(locationData).join(', ') : 'None'}</div>
        </div>

        {/* Raw Data Display */}
        {locationData && (
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800">
            <h3 className="font-bold text-lg mb-4">Raw API Response</h3>
            <pre className="text-xs text-slate-400 overflow-auto max-h-96">
              {JSON.stringify(locationData, null, 2)}
            </pre>
          </div>
        )}

        {/* Location Info */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800">
          <h2 className="text-xl font-bold mb-2">{location.name || 'Loading...'}</h2>
          <p className="text-slate-400 text-sm">{location.city || ''}, {location.state || ''}, {location.country || ''}</p>
        </div>

        {/* KPI Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="text-slate-400 text-xs mb-1">Temperature</div>
            <div className="text-2xl font-bold text-orange-400">{kpi.temperature ? kpi.temperature.toFixed(1) : '--'}°C</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="text-slate-400 text-xs mb-1">LST</div>
            <div className="text-2xl font-bold text-red-400">{kpi.lst_day ? kpi.lst_day.toFixed(1) : '--'}°C</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="text-slate-400 text-xs mb-1">NDVI</div>
            <div className="text-2xl font-bold text-emerald-400">{kpi.ndvi ? kpi.ndvi.toFixed(2) : '--'}</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="text-slate-400 text-xs mb-1">Heat Risk</div>
            <div className="text-2xl font-bold text-amber-400">{kpi.heat_risk_score ? kpi.heat_risk_score.toFixed(0) : '--'}/100</div>
          </div>
        </div>

        {/* API Link */}
        <div className="text-center text-slate-500 text-xs">
          <a href="http://127.0.0.1:8000/docs" target="_blank" className="hover:text-slate-300">
            View API Documentation →
          </a>
        </div>
      </div>
    </div>
  )
}

export default App
