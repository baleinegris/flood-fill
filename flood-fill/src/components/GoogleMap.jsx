import React, {Suspense, useContext, useEffect, useRef, useState} from 'react';
import {APIProvider, Map} from '@vis.gl/react-google-maps';
import { Loader } from '@googlemaps/js-api-loader';
import { Marker } from '@react-google-maps/api';
import Report from './Report';
import { ReportContext } from '../contexts/ReportViewContext';
import SpinnerLoad from './Spinner';

const FLASK_URL = 'temp'

const mapStyles = [
  {
    featureType: 'all',
    elementType: 'labels',
    stylers: [{ visibility: 'off' }],
  },
  {
    featureType: 'road',
    elementType: 'geometry',
    stylers: [{ visibility: 'on' }],
  },
  {
  featureType: 'road',
  elementType: 'labels',
  stylers: [{ visibility: 'on' }],
  },
  {
    featureType: 'transit',
    elementType: 'geometry',
    stylers: [{ visibility: 'off' }],
  },
  {
    featureType: 'administrative.locality',
    elementType: 'labels',
    stylers: [{ visibility: 'on' }], // Turn on labels for city names
  },
  {
    featureType: 'poi',
    elementType: 'geometry',
    stylers: [{ visibility: 'off' }],
  },
  {
    featureType: 'water',
    elementType: 'geometry',
    stylers: [{ visibility: 'on' }],
  },
];


export default function GoogleMap() {
  const [loadingReport, setLoadingReport] = useState(false);
  let count = 0;
  const viewContext = useContext(ReportContext);
  const reportView = viewContext.reportView;
  const setReportView = viewContext.setReportView;
  const setActiveReport = viewContext.setActiveReport;
  const activeReport = viewContext.activeReport;
  const inputRef = useRef(null);
  const [location, setLocation] = useState('');
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [marker, setMarker] = useState(null);
  const handleInputChange = (event) => {
    setLocation(event.target.value);
  };
  async function getData(position) {
    setTimeout(() => {
      setLoadingReport(false);
    }, 1000);
    return;
    const response = await fetch(FLASK_URL);
    const data = await response.json();
    return data;
    setLoadingReport(false);
  }
  const handleSearch = () => {
    if (window.google && window.google.maps && location) {
      const geocoder = new window.google.maps.Geocoder();
      geocoder.geocode({ address: location }, (results, status) => {
        if (status === 'OK' && results[0]) {
          console.log(results[0]);
          const position = results[0].geometry.location;
          const id = results[0].formatted_address;
          if (mapInstance) {
            map.panTo(position);
            map.setZoom(15);
            if (marker) {
              marker.setMap(null);
            }
            const newMarker = new window.google.maps.Marker({
              position,
              map,
              label: {
                text: id,
                color: 'black',
                fontSize: '16px',
                fontWeight: 'bold',
              }
            });
            setMarker(newMarker);
          }
        } else {
          console.error('Geocode was not successful for the following reason: ' + status);
        }
      });
    }
  };

  useEffect(() => {
    const loader = new Loader({
      apiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
      version: 'weekly',
      libraries: ['places']
    });

    loader.load().then(() => {
      if (mapRef.current) {
        const mapInstance = new window.google.maps.Map(mapRef.current, {
          center: { lat: 43.6532, lng: -79.3832 },
          zoom: 13,
          mapTypeId: 'hybrid',
          mapTypeControl: false,
          styles: mapStyles,
        });
        setMap(mapInstance);
        // AUTOCOMPLETE
        const autocomplete = new window.google.maps.places.Autocomplete(inputRef.current);
        autocomplete.bindTo('bounds', mapInstance);
        autocomplete.addListener('place_changed', () => {
          const place = autocomplete.getPlace();
          if (!place.geometry || !place.geometry.location) {
            console.log('No details available for input: ' + place.name);
            return;
          }
          const position = place.geometry.location;
          setReportView(true);
          setLoadingReport(true);
          getData(position);
          const id = place.formatted_address;
          setLocation(id);
          if (mapInstance) {
            console.log('test')
            mapInstance.panTo(position);
            mapInstance.setZoom(15);
            if (marker) {
              marker.setMap(null);
            }
            const newMarker = new window.google.maps.Marker({
              id: count,
              position,
              map: mapInstance,
              label: {
                text: id,
                className: "map-label",
                fontSize: '16px',
                fontWeight: 'bold',
              }
            });
            i += 1;
            setMarker(newMarker);
            newMarker.addListener("click", () => {
              setActiveReport(newMarker.id);
            });
          }
        });
      }
    }).catch(e => {
      console.error('Error loading Google Maps API:', e);
    });
  }, [mapRef]);


    return (
      <>
      <div className='bg-white backdrop-blur-sm px-5 pb-5 m-5 rounded-lg border-black border-[1px] left-0'>
      <input className='m-4 p-2 z-10 relative bg-slate-500 border-black border-2 text-black' ref={inputRef} type="text" placeholder="Type in an address!" onChange={handleInputChange}/>
      <button className='relative border-black border-1' onClick={handleSearch}> Search! </button>
      <div ref={mapRef} style={{ width: '60vw', height: '80vh' }} />
      </div>
      {reportView && 
      <div className='flex w-full h-full justify-center items-center'>
        {loadingReport ? <SpinnerLoad/> : <Report name={location} precipitation={33}/>}
      </div>}
      </>
    )
}