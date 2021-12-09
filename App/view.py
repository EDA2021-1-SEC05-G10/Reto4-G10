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

import prettytable
import config as cf
import sys
import controller
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.ADT import queue as q
from DISClib.ADT import stack as st
assert cf
from prettytable import PrettyTable

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
    print("7- La ruta mas corta entre ciudades con ayuda de API")
    print("0- Salir")


catalog = None

def cargaDatos():
    catalog= controller.init()
    sys.setrecursionlimit(8650000)
    controller.loadServices(catalog)
    controller.loadRutes(catalog)
    controller.loadCities(catalog)
    controller.loadGraph(catalog)
    rta= controller.loadDatos(catalog)
    tabla1 = PrettyTable()
    tabla1.field_names = ["Nombre", "Ciudad","País","Latitud","Longitud"]
    tabla2 = PrettyTable()
    tabla2.field_names = ["Nombre", "Población","Latitud","Longitud"]
    print('El total de aeropuertos en cada grafo es: '+ str(rta[0]))
    print('\n El total de rutas aéreas en cada grafo es: '+str(rta[1]))
    print('\n El total de ciudades: '+str(rta[2]))
    print('\n El primer aeropuerto cargado es: ')
    t1 = [str(rta[3]['Name']),str(rta[3]['City']),str(rta[3]['Country']),str(rta[3]['Latitude']),str(rta[3]['Longitude'])]
    tabla1.add_row(t1)
    print(tabla1)
    print('\n La informacion de la ultima ciudad cargada es: ')
    t2 = [str(rta[4]['city']),str(rta[4]['population']),str(rta[4]['lat']),str(rta[4]['lng'])]
    tabla2.add_row(t2)
    print(tabla2)
    return catalog

def requerimiento1():
    reque1=controller.requerimiento1(catalog)
    print("La cantidad de aeropuertos interconectados es "+ str(lt.size(reque1)))
    tabla1 = PrettyTable()
    tabla1.field_names = ["Nombre", "Ciudad","País","IATA","Cant Vuelos","inbound","outbound"]
    tabla1._max_width={"Nombre":20,"Ciudad":17,"País":15,"IATA":10 ,"Cant Vuelos":10,"inbound":10,"outbound":10}
    for i in range(lt.size(reque1)):
        datos = [lt.getElement(reque1, i)[0]['Name'],lt.getElement(reque1, i)[0]['City'],lt.getElement(reque1, i)[0]['Country'],
                lt.getElement(reque1, i)[0]['IATA'],str(lt.getElement(reque1, i)[1]),str(lt.getElement(reque1, i)[2]),
                str(lt.getElement(reque1, i)[3])]
        tabla1.add_row(datos)
    print(tabla1)
        

def requerimiento2(iata1, iata2):
    reque2=controller.requerimiento2(catalog, iata1, iata2)
    print('El Numero total de SCC en la red de rutas del aeropuerto es: '+ str(reque2[1]))
    print('El aeropuerto de Pulkovo y el aeropuerto de Rutland Plains van juntos ?')
    print(reque2[0] + '\n')

def requerimiento3(ciudadA, ciudadB):
    reque3=controller.requerimiento3(catalog,ciudadA, ciudadB)
    if reque3 is not None:
        print(str(reque3[0]) + '\n')
        print(str(reque3[1]) + '\n')
        print(str(reque3[2]+reque3[3]+reque3[5])+ '\n')
        for i in range(st.size(reque3[4])):
            print(st.pop(reque3[4]) + '\n')

def requerimiento4(ciudad_origen, millas):
    reque4=controller.requerimiento4(catalog,ciudad_origen, millas)
    print(reque4[1])
    print('El numero total de nodos conectados es: '+ str(q.size(reque4[0])))
    print('El costo total es: '+ str(reque4[1]))
    print('La cantidad de millas requeridas son: '+ str(reque4[2]))
    tabla1 = PrettyTable()
    tabla1.field_names = ["Departiture", "Destination","Km"]
    for i in range(q.size(reque4[0])):
        x = q.dequeue(reque4[0])
        datos = [x["vertexA"],x["vertexB"],x["weight"]]
        tabla1.add_row(datos)
    print(tabla1)

def requerimiento5(aeropuerto):
    reque5=controller.requerimiento5(catalog, aeropuerto)
    print(lt.size(reque5))
    tabla1 = PrettyTable()
    tabla1.field_names = ["IATA", "Name","City","Country"]
    for i in range(1,lt.size(reque5)) :
        x=lt.getElement(reque5,i)
        datos = me.getValue(mp.get(catalog["stops"],x["Destination"]))
        datos = [datos["IATA"],datos["Name"],datos["City"],datos["Country"]]
        tabla1.add_row(datos)
    print("Los aeropuertos afectados son: ")
    print(tabla1)

def requerimiento6(origen,destino):
    recorrido, distancia=controller.requerimiento6(catalog, origen, destino)
    print("La distancia total es: " +str(distancia))
    print("La ruta final es: \n")
    i = 1
    lista = []
    for cada in lt.iterator(recorrido):
        if i == 1:
            lista.append(cada["vertexA"])
            lista.append(cada["vertexB"])
        else:
            lista.append(cada["vertexB"])
        i+=1
    print("La ruta final es: \n")
    print(lista)

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

    elif int(inputs[0]) == 7:
        origen = input("Ingrese ciudad de origen")
        destino = input("Ingrese ciudad de destino")
        requerimiento6(origen,destino)

    else:
        sys.exit(0)
sys.exit(0)

