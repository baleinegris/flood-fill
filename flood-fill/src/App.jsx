import React, { useState, useEffect, createContext, useContext } from 'react'
import './App.css'
import Title from './components/Title'
import Map from './components/GoogleMap';
import {APIProvider} from '@vis.gl/react-google-maps';
import GoogleMap from './components/GoogleMap';
import Particles from './components/Particles';
import { ReportProvider, ReportContext } from './contexts/ReportViewContext';
function App() {
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

  useEffect(() => {
    console.log('API Key:', apiKey);
  }, [apiKey]);

  return (
    <div id='app' className='w-[100vw] bg-slate-300	'>
    <ReportProvider>
      <APIProvider apiKey={apiKey} onLoad={() => console.log('Maps API has loaded.')}>
        <Title />
        <div className='flex items-center w-[100%] relative justify-center'>
          <GoogleMap />
          <ReportMessage/>
          </div>
      </APIProvider>
    </ReportProvider>
    </div>
  )
}

const ReportMessage = () => {
  const { reportView } = React.useContext(ReportContext);

  return (
    !reportView && (
      <div className='relative text-white w-[200px] p-6 rounded-xl bg-purple-950 font-bold border-black border-4'>
        Welcome to Flood Fill! Enter a location to generate a report of its expected flood risk in the future!
      </div>
    )
  );
};

export default App
