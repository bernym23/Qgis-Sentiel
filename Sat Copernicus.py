#Este script nos permite cargar imagenes Sentinel 2 al Canvas de Qgis, utilizando Google Earth Engine y Python

#llamado al plugin
import ee

#Para autenticar ejecutamos, solo se hace una vez
ee.Authenticate()

#Para iniciar el plugin
ee.Initialize()

#Llamado dentro del plugin al mapa
from ee_plugin import Map

#Aplicar la funcion de la mascara de nube
def maskS2clouds(image):
    #Se seleciiona la banda de mascara de nubes
    qa = image.select('QA60')

    # del 0,1.  1 trata de limpiar las nubes.
    cloudBitMask = 8 << 10
    cirrusBitMask = 11 << 11
    #esto lo tiene que arreglar, forma de concatenar en phython#

    # las 2 en cero quiere decir que esta "despejado"
    mask = qa.bitwiseAnd(cloudBitMask).eq(0),
    (qa.bitwiseAnd(cirrusBitMask).eq(0));
    
    #Aquí se devuelve el valor de las mascaras
    return image.updateMask(mask).divide(10000)


#llamada a la coleccion, vamos a declarar la variable Sat.
Sat = (ee.ImageCollection('COPERNICUS/S2_SR')
#Para imagenes del 2022 en adelante usar
#Sat = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
           
              # Aquí se cambian las fechas.
              .filter(ee.Filter.date('2021-8-1', '2021-8-30'))
              # Poner el rango de nubosidad maxima
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',50 ))
              # aplicar la mascara de nubes.
              .map(maskS2clouds)
             )

#Aquí se cambian las bandas a visualizar

#Bandas 4,3,2 son imagenes en RGB
visParams1 = {
    'min' : 0,
    'max' : 0.3,
    'bands' : ['B4', 'B3', 'B2']}
# Aquí se agrega el mapa RGB al canvas
Map.addLayer(Sat.mean(),visParams1,"RGB")

#estos son los parametros para agregar la imagen NIR
visParams2 = {
    'min' : 0,
    'max' : 0.5,
    'bands' : ['B6', 'B3', 'B2']}
 #con esto agregamos el mapa NIR al Canvas 
Map.addLayer(Sat.mean(),visParams2,"NIR") 

#Vamos a calcular el NDVI

#Aquí hago un llamado a la imagen y uso filtros que puse anteriormente
#recordemos que 'sat' es la variable de la imagen satelital
Tiempo1b = Sat.reduce(ee.Reducer.median());

#Calculamos el NDVI
NDVI1 = Tiempo1b.normalizedDifference (['B8_median', 'B4_median']);

#Vamos a darle color
visParams3 = {
  'min' : 0,
  'max' : 1.0,
  
  'palette' : ['CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901', '66A000', '529400', '3E8601',
    '207401', '056201', '004C00', '023B01', '012E01', '011D01', '011301']
}
#Agregamos al canvas como otro layer y le ponemos como nombre NDVI
Map.addLayer (NDVI1,visParams3, 'NDVI');

#Aquí se centra el mapa en Venecia, con un zoom de 12   
Map.setCenter(-84.25272, 10.36041,12)
