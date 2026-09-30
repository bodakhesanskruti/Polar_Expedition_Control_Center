import { useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './LiveMap.css';

function MapSizeObserver() {
  const map = useMap();

  useEffect(() => {
    // Leaflet calculates tile layout on mount. Recalculate whenever the
    // dashboard grid, sidebar or browser viewport changes the map size.
    const container = map.getContainer();
    const resizeObserver = new ResizeObserver(() => {
      map.invalidateSize({ pan: false, debounceMoveend: true });
    });

    resizeObserver.observe(container);
    const frame = window.requestAnimationFrame(() => {
      map.invalidateSize({ pan: false });
    });

    return () => {
      resizeObserver.disconnect();
      window.cancelAnimationFrame(frame);
    };
  }, [map]);

  return null;
}

export default function LiveMap({ live }) {
  const cargo = live?.cargo || [];
  const personnel = live?.personnel || [];

  // Antarctica operations: Leaflet coordinates are [latitude, longitude].
  const center = [-72.0, 2.0];

  return (
    <div className="map liveMapSurface">
      <MapContainer
        center={center}
        zoom={2}
        minZoom={2}
        maxZoom={12}
        scrollWheelZoom={false}
        zoomControl={false}
        preferCanvas
        className="leafletMissionMap"
      >
        <MapSizeObserver />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {cargo.map((item, index) => (
          <CircleMarker
            key={`cargo-${item.cargo_id ?? index}`}
            center={[Number(item.latitude), Number(item.longitude)]}
            radius={7}
            pathOptions={{
              color: '#72c9f2',
              weight: 2,
              fillColor: '#329ed8',
              fillOpacity: 0.95,
            }}
          >
            <Popup>
              <strong>Cargo #{item.cargo_id ?? '—'}</strong>
              <br />Status: {item.status || 'Unknown'}
              {item.mode && <><br />Mode: {item.mode}</>}
            </Popup>
          </CircleMarker>
        ))}

        {personnel.map((item, index) => {
          const status = String(item.status || '').toLowerCase();
          const attention = ['alert', 'offline', 'missing', 'sos'].some((s) => status.includes(s));
          return (
            <CircleMarker
              key={`person-${item.personnel_id ?? index}`}
              center={[Number(item.latitude), Number(item.longitude)]}
              radius={7}
              pathOptions={{
                color: attention ? '#f4c15b' : '#69e0bb',
                weight: 2,
                fillColor: attention ? '#e5a92e' : '#2fc69b',
                fillOpacity: 0.95,
              }}
            >
              <Popup>
                <strong>Personnel #{item.personnel_id ?? '—'}</strong>
                <br />Status: {item.status || 'Unknown'}
                {item.expedition_id != null && <><br />Expedition: {item.expedition_id}</>}
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
}
