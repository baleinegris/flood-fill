import { useState, useEffect } from 'react'
import './App.css'
import Title from './components/Title'
import Map from './components/GoogleMap';
import {APIProvider} from '@vis.gl/react-google-maps';
import GoogleMap from './components/GoogleMap';
import AutoSearch from './components/AutoSearch';

function App() {
  const [count, setCount] = useState(0)
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

  useEffect(() => {
    console.log('API Key:', apiKey);
  }, [apiKey]);

  return (
    <>
    <APIProvider apiKey={apiKey} onLoad={() => console.log('Maps API has loaded.')}>
      <AutoSearch/>
      <Title />
      <GoogleMap />
    </APIProvider>
    </>
  )
}

export default App
