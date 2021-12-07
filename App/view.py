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
from DISClib.ADT import queue as q
from DISClib.ADT import stack as st
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
    sys.setrecursionlimit(8650000)
    controller.loadServices(catalog)
    controller.loadRutes(catalog)
    controller.loadCities(catalog)
    controller.loadGraph(catalog)
    rta= controller.loadDatos(catalog)
    print('El total de aeropuertos en cada grafo es: '+ str(rta[0]))
    print('\n El total de rutas aéreas en cada grafo es: '+str(rta[1]))
    print('\n El total de ciudades: '+str(rta[2]))
    print('\n El primer aeropuerto cargado es: '+str(rta[3]['Name'])+ 'ciudad: '+str(rta[3]['City'])+ 'pais: '+ str(rta[3]['Country'])+ 
    'latitud y longitud: '+ str(rta[3]['Latitude'])+ ', '+ str(rta[3]['Longitude']))
    print('\n La informacion de la ultima ciudad cargada es: '+ str(rta[4]['city'])+'Su ppoblacion es de: ' + str(rta[4]['population'])+
    'latitud y longitud'+ str(rta[4]['lat'])+', ' +str(rta[4]['lng']))

    return catalog

def requerimiento1():
    reque1=controller.requerimiento1(catalog)
    print("La cantidad de aeropuertos interconectados es "+ str(lt.size(reque1)))
    for i in range(lt.size(reque1)):
        print('El nombre es: '+ lt.getElement(reque1, i)[0]['Name'])
        print('La ciudad es: '+ lt.getElement(reque1, i)[0]['City'])
        print('El pais es: '+ lt.getElement(reque1, i)[0]['Country'])
        print('El codigo IATA es: '+ lt.getElement(reque1, i)[0]['IATA'])
        print('La cantidad de vuelos es: '+lt.getElement(reque1, i)[1])
        print('El numero de vuelos entrados es: '+lt.getElement(reque1, i)[2])
        print('El numero de vuelos salidos es: '+lt.getElement(reque1, i)[3])
        
        

def requerimiento2(iata1, iata2):
    reque2=controller.requerimiento2(catalog, iata1, iata2)
    print(reque2[0] + '\n')
    print('El total de componentes conectados es: '+ str(reque2[1]))

def requerimiento3(ciudadA, ciudadB):
    reque3=controller.requerimiento3(catalog,ciudadA, ciudadB)
    print(str(reque3[0]) + '\n')
    print(str(reque3[1]) + '\n')
    print(str(reque3[2]+reque3[3]+reque3[5])+ '\n')
    for i in range(st.size(reque3[4])):
        print(st.pop(reque3[4]) + '\n')

def requerimiento4(ciudad_origen, millas):
    reque4=controller.requerimiento4(catalog,ciudad_origen, millas)
    print('El numero total de nodos conectados es: '+ str(q.size(reque4[0])))
    print('El costo total es: '+ str(reque4[1]))
    print('La cantidad de millas excendetes es: '+ str(reque4[2]))
    for i in range(q.size(reque4[0])):
        print(q.dequeue(reque4[0]))
        

def requerimiento5(aeropuerto):
    reque5=controller.requerimiento5(catalog, aeropuerto)
    print(lt.size(reque5))
    for element in reque5:
        print(element + '\n')






"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog=cargaDatos()
        
    elif int(inputs[0]) == 2:
       requerimiento1()
       
    elif int(inputs[0]) == 3:
        iata= input('Ingrese codigo IATA aeropuerto1: ')
        iata2= input('Ingrese codigo IATA aeropuerto2: ')
        requerimiento2(iata, iata2)

    elif int(inputs[0]) == 4:
        ciudad= input('Ingrese ciudad de origen: ')
        ciudad2= input('Ingrese ciudad de destino: ')
        requerimiento3(ciudad, ciudad2)

    elif int(inputs[0]) == 5:
        ciudad= input('Ingrese ciudad de origen: ')
        millas= input('Ingrese cantidad de millas: ')
        requerimiento4(ciudad, millas)

    elif int(inputs[0]) == 6:
        codigo= input('Ingrese codigo IATA aeropuerto1: ')
        requerimiento5(codigo)



    else:
        sys.exit(0)
sys.exit(0)
