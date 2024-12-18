var geometry = 
    /* color: #08d698 */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[-66.28895224928985, -23.698266741998257],
          [-66.28929557204376, -23.77589350579841],
          [-66.18286551833282, -23.77495094817278],
          [-66.1818355500711, -23.69763799652877]]]),
    imageCollection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED");

// Definir geometría (Región de Interés - ROI)
Map.centerObject(geometry, 10);
Map.addLayer(geometry, {color: 'blue'}, 'Región de Interés (Salinas Grandes)');

// Cargar colección Sentinel-2 SR Harmonized
var sentinel_2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterDate("2023-12-21", "2024-03-20") // Filtro por fecha
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) // Filtro por nubosidad
    .filterBounds(geometry); // Filtro por geometría

print(sentinel_2);
print("Número de imágenes disponibles:", sentinel_2.size());


var img_S2 = sentinel_2.median();
var img_S2_C = img_S2.clip(geometry);
Map.addLayer(img_S2_C, {
  min: 0,
  max: 5000,
  gamma: 0.5,
  bands: ["B6", "B5", "B4"]
}, "Imagen RGB");

// Cálculo de índices
var NDVI = img_S2_C.expression(
  "(NIR-RED)/(NIR+RED)",
  {
    "NIR": img_S2_C.select("B8"), 
    "RED": img_S2_C.select("B4")
  }
);



// **Cálculo del Índice Salino (IS)
var IS = img_S2_C.expression(
  "(B2 - B4) / (B2 + B4)", 
  {
    'B2': img_S2_C.select('B2'),  // Banda Azul
    'B4': img_S2_C.select('B4')   // Banda Roja
  }
);

// Estadísticas para IS
var stats_is = IS.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: geometry,
  scale: 10,
  maxPixels: 1e8
});

// Visualización mejorada
var viss_ndvi = {min: -0.2, max: 0.3, palette: ['white', 'yellow', 'green']};


Map.addLayer(NDVI, viss_ndvi, "NDVI");



// Visualización del Índice Salino (IS)
var viss_is = {min: -1, max: 1, palette: ['blue', 'white', 'red']};
Map.addLayer(IS, viss_is, "Índice Salino (IS)");

// Exportar el Índice Salino (IS)
Export.image.toDrive({
  image: IS,
  description: 'IS_Salinas_Grandes_2024',
  region: geometry,
  scale: 10,
  maxPixels: 1e8
});

// Exportar el NDVI
Export.image.toDrive({
  image: NDVI,
  description: 'NDVI_Salinas_Grandes_2024',
  region: geometry,
  scale: 10,
  maxPixels: 1e8
});
