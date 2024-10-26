import React, {useEffect, useRef, useState} from 'react';
import {APIProvider, Map} from '@vis.gl/react-google-maps';
import { Loader } from '@googlemaps/js-api-loader';
import { Marker } from '@react-google-maps/api';
import Report from './Report';
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
  const inputRef = useRef(null);
  const [location, setLocation] = useState('');
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [marker, setMarker] = useState(null);
  const [searched, setSearched] = useState(false);

  const handleInputChange = (event) => {
    setLocation(event.target.value);
  };

  const handleSearch = () => {
    if (window.google && window.google.maps && location) {
      const geocoder = new window.google.maps.Geocoder();
      geocoder.geocode({ address: location }, (results, status) => {
        if (status === 'OK' && results[0]) {
          setSearched(true);
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
          console.log(map)
          const position = place.geometry.location;
          setSearched(true);
          const id = place.formatted_address;
          if (mapInstance) {
            console.log('test')
            mapInstance.panTo(position);
            mapInstance.setZoom(15);
            if (marker) {
              marker.setMap(null);
            }
            const newMarker = new window.google.maps.Marker({
              position,
              map: mapInstance,
              label: {
                text: id,
                color: 'black',
                fontSize: '16px',
                fontWeight: 'bold',
              }
            });
            setMarker(newMarker);
          }
        });
      }
    }).catch(e => {
      console.error('Error loading Google Maps API:', e);
    });
  }, [mapRef]);


    return (
      <div>
      <input className='m-4 p-2 z-10 relative' ref={inputRef} type="text" placeholder="Type in an address!" onChange={handleInputChange}/>
      <button className='relative' onClick={handleSearch}> Search! </button>
      <div ref={mapRef} style={{ width: '60vw', height: '80vh' }} />
      {searched && <div> Report for location : {location} </div>}
      {searched && 
      <div className='flex w-full h-full justify-center items-center'>
        <Report name={location} precipitation={33}/>
      </div>}
      </div>
    )
}