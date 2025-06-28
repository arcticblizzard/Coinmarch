# Map of Kolnmark

![](../images/kolnmark_panorama.jpg)

<div id="map" style="height: 600px;"></div>

<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>
<script
  src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js">
</script>

<script>
  var map = L.map('map', {
    crs: L.CRS.Simple,
    minZoom: -5,
    maxZoom: 2,
    zoomSnap: 0.5
  });

  var bounds = [[0, 0], [6525, 9960 ]];

  // Add the image
  L.imageOverlay("/Coinmarch/images/kolnmark.jpg", bounds).addTo(map);

  // Fit view to image bounds (zoomed out)
  map.fitBounds(bounds);
</script>
