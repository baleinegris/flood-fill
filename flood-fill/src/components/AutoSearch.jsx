import {useEffect, useRef, useMemo} from 'react';
import {Loader} from '@googlemaps/js-api-loader';
export function AutoSearch() {
  const googlemap = useRef(null);

  useEffect(() => {
    const loader = new Loader({
      apiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
      version: 'weekly',
      libraries: ['places'],
    });
    let map;
    loader.load().then(() => {
        const google = window.google;
        const service = new google.maps.places.AutocompleteService();
        map = new google.maps.Map(googlemap.current, {
            center: {lat: -34.397, lng: 150.644}, // or anywhere you want to show on the map by defaul
            zoom: 8, // or any other zoom level
        });
        console.log(map);
    });
  });
  return (
    <div id="map" ref={googlemap} />
  );
}

export default AutoSearch