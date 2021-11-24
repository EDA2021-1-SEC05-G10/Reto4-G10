"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar puntos de interconexión aérea")
    print("3- Encontrar clústeres de tráfico aéreo")
    print("4- Encontrar la ruta más corta entre ciudades")
    print("5- Utilizar las millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")


catalog = None

def cargaDatos():
    catalog= controller.init()
    controller.loadServices(catalog)
    controller.loadRutes(catalog)
    controller.loadCities(catalog)
    rta= controller.loadDatos(catalog)
    print('El total de aeropuertos en cada grafo es: '+ str(rta[0]))
    print('\n El total de rutas aéreas en cada grafo es: '+str(rta[1]))
    print('\n El total de ciudades: '+str(rta[2]))
    print('\n El primer aeropuerto cargado es: '+str(rta[3]['Name'])+ 'ciudad: '+str(rta[3]['City'])+ 'pais: '+ str(rta[3]['Country'])+ 
    'latitud y longitud: '+ str(rta[3]['Latitude'])+ ', '+ str(rta[3]['Longitude']))
    print('\n La informacion de la ultima ciudad cargada es: '+ str(rta[4]['city'])+'Su ppoblacion es de: ' + str(rta[4]['population'])+
    'latitud y longitud'+ str(rta[4]['lat'])+', ' +str(rta[4]['lng']))

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        cargaDatos()
    elif int(inputs[0]) == 2:
        pass

    else:
        sys.exit(0)
sys.exit(0)
