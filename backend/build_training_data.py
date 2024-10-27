import fiona

with fiona.open('\data\floods\historical_flood_events.gpkg') as src:
        print(src.schema)
        floods = set()
        for feature in src:
            floods.add({'year': feature['properties']['year'], 'longitude': feature['geometry']['coordinates'][0], 'latitude': feature['geometry']['coordinates'][1]})
        print(floods)

