let mapInstance = null; // Store map instance globally for reference

// Final, robust map initialization script using a timeout for guaranteed rendering
document.addEventListener('DOMContentLoaded', function() {
    
    // CRITICAL: Wrap the entire initialization process in a small timeout (50ms)
    // to ensure the DOM has completed its layout calculations, fixing the white box issue.
    setTimeout(function() {
        const dataElement = document.getElementById('attractions_data');
        let attractionData = [];
        
        if (dataElement && dataElement.textContent.trim().length > 0) {
            try {
                attractionData = JSON.parse(dataElement.textContent.trim());
            } catch (e) {
                console.error("Error parsing attraction data:", e);
            }
        }

        if (typeof L === 'undefined') {
            console.error("Leaflet.js not loaded.");
            return;
        }

        const defaultLat = 7.1907;
        const defaultLon = 125.4550;
        const defaultZoom = 10;

        // Check if map instance already exists and remove it to prevent errors
        let mapContainer = document.getElementById('attractionMap');
        if (mapContainer._leaflet_id) {
            mapContainer._leaflet_id = null; 
        }

        const map = L.map('attractionMap').setView([defaultLat, defaultLon], defaultZoom);
        mapInstance = map; // Store new instance

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        let hasMarkers = false;
        let markers = [];

        attractionData.forEach(function(attraction) {
            const lat = parseFloat(attraction.latitude);
            const lon = parseFloat(attraction.longitude);
            
            // Marker plotting logic (including the check for Null Island)
            if (lat !== 0 && lon !== 0) {
                hasMarkers = true;
                
                const detailUrl = `/attractions/${attraction.id}/`;

                const popupContent = `
                    <div class="font-sans text-sm">
                        <h3 class="font-bold text-davao-dark">${attraction.name}</h3>
                        <p class="text-gray-700">${attraction.location}</p>
                        <a href="${detailUrl}" class="text-blue-600 hover:text-blue-800 font-medium">View Details</a>
                    </div>
                `;

                const marker = L.marker([lat, lon])
                    .addTo(map)
                    .bindPopup(popupContent);
                
                markers.push(L.latLng(lat, lon));
            }
        });

        // CRITICAL: Forces the map to re-evaluate its size and draw tiles
        map.invalidateSize();

        if (hasMarkers && markers.length > 0) {
            const bounds = L.latLngBounds(markers);
            map.fitBounds(bounds, { padding: [50, 50] });
        }
    }, 50); // Small delay to guarantee DOM rendering is complete
});