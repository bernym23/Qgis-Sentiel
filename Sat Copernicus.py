
#llamado al plugin
import ee
#Llamado dentro del plugin al mapa
from ee_plugin import Map
#Aplicar la funcion de la mascara de nube
def maskS2clouds(image):
    #Se seleciiona la banda de mascara de nubes
    qa = image.select('QA60')

    # del 0,1.  1 trata de limpiar las nubes.
    cloudBitMask =8<< 10
    cirrusBitMask = 11 << 11
    #esto lo tiene que arreglar, forma de concatenar en phython#

    # las 2 en cero quiere decir que esta "despejado"
    mask = qa.bitwiseAnd(cloudBitMask).eq(0),
    (qa.bitwiseAnd(cirrusBitMask).eq(0));
    
    #Aquí se devuelve el valor de las mascaras
    return image.updateMask(mask).divide(10000)


# llamada a las imaganes de Sat
Sat = (ee.ImageCollection('COPERNICUS/S2_SR')
           
              # Aquí se cambian las fechas.
              .filter(ee.Filter.date('2021-1-1', '2021-1-30'))
              # Poner el rango de nubosidad maxima
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',40 ))
              # aplicar la mascara de nubes.
              .map(maskS2clouds)
             )

 

#Aquí se cambian las bandas a visualizar
#Bandas 4,3,2 son imagenes en RGB
visParams1 = {
    'min' : 0,
    'max' : 0.3,
    'bands' : ['B4', 'B3', 'B2']}

#Aquí se centra el mapa en Venecia, con un zoom de 12   
#Map.setCenter(-84.25272, 10.36041,12)

# Aquí se agrega el mapa RGB al canvas
Map.addLayer(Sat.mean(),visParams1,"RGB")

#estos son lo9s parametros para agregar la imagen NIR
#visParams2 = {
   # 'min' : 0,
    #'max' : 0.3,
    #'bands' : ['B8', 'B3', 'B2']}
 
#con esto agregamos el mapa NIR al Canvas 
#Map.addLayer(Sat.mean(),visParams2,"NIR") 
#Como futura actualizacion: 
#script está pendiente el delimitado del resultado, corte solo a Costa Rica
#multiples vistas cargadas al Canvas, tanto RGB como NIR
#Como opcional el enlace de descarga
