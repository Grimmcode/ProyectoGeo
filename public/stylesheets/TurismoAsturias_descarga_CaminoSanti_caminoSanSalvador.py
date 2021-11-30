#importamos librerias
from bs4 import BeautifulSoup
import requests
import urllib.request
import re ##para trabajar con strings

#Variables
enlaces_rutas = [] #enlaces de las rutas a las paginas web donde se encuentran los kml
nombres_archivos = []
cabecera_url = ['https://www.turismoasturias.es','']
url_separadas_archivos = '' #url de los archivos kml separados sin cabecera
url_descarga_archivo = '' #url completa para descargar el archivo

##variables para los strings de los nombres
nombres_limpios = []
nombres = []


#-- OBTENCION ENLACES DE PAGINAS --#
#Enlace de rutas de senderismo
url_rutas_CS_salvador = 'https://www.turismoasturias.es/camino-de-santiago/camino-san-salvador'

#Obtenemos el contenido de la url
contenido_url_CS_salvador = requests.get(url_rutas_CS_salvador)

#Hacemos un parseo para obtener el contenido en formato html
html_CS_salvador= BeautifulSoup(contenido_url_CS_salvador.content, 'html.parser')

#Obtenemos los enlaces a las paginas donde se encuentran los archivos kml con las rutas de senderismo
#que se encuentran dentro de las etiquetas html <a></a>
etiquetas_rutas = html_CS_salvador.find_all('a', class_='link')

#obtemos las url de cada una de las rutas de senderismo
for enlaces in etiquetas_rutas:
    enlaces_rutas.append(enlaces.get("href"))

# ---> Obtencion de nombres para los archivos
#Obtenemos las etiquetas con los nombres de los archivos
etiquetas_nombre = html_CS_salvador.find_all('span', class_="title")
for names in etiquetas_nombre:
     nombres_archivos.append(names.text)

for i in range(len(nombres_archivos)):
    nombres_limpios.append(re.sub("\\n|\\t|\:|\-|\/","",nombres_archivos[i]))

for j in range(len(nombres_limpios)):
    nombres.append(re.sub(" ","",nombres_limpios[j]))
#@comprueba que la lista de nombres no tiene espacios ni carácteres raros
#@print(nombres)




#-- DESCARGA DE ARCHIVOS --#
contador = 0
ciclo = 0
while contador < len(nombres_archivos):
    #descargamos los contenidos de las paginas donde se encuentran los kml para posteriormente descargarlo
    for i in range(len(enlaces_rutas)):
        #@--> comprueba que entran correctamente los enlaces
        #@print("enlace entra: ", enlaces_rutas[i])

        #realizamos un get a la url
        paginas_rutas_CS_salvador = requests.get(enlaces_rutas[i])
        #@--> comprueba que la conexion se realiza correctamente, resultado: response[200]
        #@print("paginas todas: ", paginas_rutas_senderismo)

        #transformamos a formato BeautifulSoup para poder identificar diferentes elementos del documento html y acceder a ellos
        ##le pasamos la pagina y hacemo un parse a html 
        pagina_unica = paginas_rutas_CS_salvador
        #@--> comprueba que la conexion se realiza correctamente, resultado: response[200]
        #@print("pagina unica: ", pagina_unica)

        #parseo del contenido de la pagina a html
        html_pag_rutas = BeautifulSoup(pagina_unica.content, 'html.parser')

        #especificar el barra baja en clase para que no interprete que se está creando una clase
        #obtenemos las etiquetas con las rutas de los archivos  
        etiquetas_kml = html_pag_rutas.find_all('a', class_='file-kml')
        #@comprueba que se recogen tanto el enlace para kml como para gpx
        #@print("url kml: ",url_kml)
        

        ##extraemos las rutas donde se encuentran los archivos kml, los hipervinculos
        for rutas in etiquetas_kml:
            #obtencion de las rutas
            url_separadas_archivos = rutas.get("href")
            #@comprueba que obtenemos las rutas de descarga del archivo kml y gpx: 36 rutas
            #@print("url ruta:",url_separadas_archivos)
                
            #introducimos en una lista junto  a la cabecera cada una de las rutas a los archivos kml
            cabecera_url[1] = url_separadas_archivos
                
            #realizamos la union de la cabecera y la ruta para obtener el enlace completo
            url_descarga_archivo = "".join(cabecera_url)
            #@comprueba que las rutas se hayan generado correctamente
            #@print("ruta descarga: ", url_descarga_archivo)

            #creamos la ruta de la carpeta donde se va a guardar el archivo y le añadimos el nombre del archivo con la extension
            ruta_carpeta ='D:/Proyectos_Trabajos/ProyAppGeo/Proyecto_2021_2022/datos/TurismoAsturias/caminoSantiago/caminoSanSalvador'+nombres[contador] +".kml"
            contador = contador + 1
            print("ruta carpeta: ", ruta_carpeta)

            #realizamos la descarga de los archivos
            urllib.request.urlretrieve(url_descarga_archivo, ruta_carpeta)