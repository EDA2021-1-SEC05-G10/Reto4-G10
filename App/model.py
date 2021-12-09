"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from os import system
import sys
from DISClib.Algorithms.Graphs.bfs import bfsVertex
from DISClib.DataStructures.adjlist import vertices
from DISClib.DataStructures.arraylist import newList
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import graph as gr
from DISClib.Utils import error as error
import DISClib.DataStructures.linkedlistiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from math import *
from DISClib.Algorithms.Graphs import prim as pr
assert cf
import requests

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    try:
        analyzer = {
                    'stops': None,
                    'connections': None,
                    'rutes': None,
                    'cities': None,
                    'components': None,
                    'paths': None,
                    'ult_pos': None,
                    'prim_pos': None,
                    'direct': None
                    }

        analyzer['stops'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStops)
        analyzer['rutes'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStops)
        analyzer['exitrutes'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStops)
        analyzer['cities'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareCities)
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=93000,
                                              comparefunction=compareStops)
        analyzer['direct'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=93000,
                                              comparefunction=compareStops)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo
def add_stops(infostop, catalog):
    if catalog['prim_pos'] is None:
        catalog['prim_pos']= infostop
    info= mp.get(catalog['stops'], infostop['IATA'])
    if info is None:
        mp.put(catalog['stops'],infostop['IATA'],infostop)
        gr.insertVertex(catalog['connections'], infostop['IATA'])
        gr.insertVertex(catalog['direct'], infostop['IATA'])
        
def add_rutes(inforutes, catalog):
    info= mp.get(catalog['rutes'], inforutes['Departure'])
    if info is None:
        rutes= lt.newList('SINGLE_LINKED')
        lt.addLast(rutes, inforutes)
        mp.put(catalog['rutes'],inforutes['Departure'],rutes)
    else:
        lt.addLast(info['value'],inforutes)
    gr.addEdge(catalog['connections'], inforutes['Departure'], inforutes['Destination'], float(inforutes['distance_km']))

def add_exit_rutes(inforutes, catalog):
    info= mp.get(catalog['exitrutes'], inforutes['Destination'])
    if info is None:
        rutes= lt.newList('SINGLE_LINKED')
        lt.addLast(rutes, inforutes)
        mp.put(catalog['exitrutes'],inforutes['Destination'],rutes)
    else:
        lt.addLast(info['value'],inforutes)

def add_cities(infocities, catalog):
    info= mp.get(catalog['cities'], infocities['city_ascii'])
    catalog['ult_pos']=infocities
    if info is None:
        mp.put(catalog['cities'],infocities['city_ascii'],infocities)

def add_graph(infodirect, catalog):
    if scc.stronglyConnected(catalog['components'], infodirect['Departure'], infodirect['Destination'] ):
        if gr.getEdge(catalog['direct'], infodirect['Departure'], infodirect['Destination']) is None or gr.getEdge(catalog['direct'], infodirect['Destination'], infodirect['Departure']) is None :
            gr.addEdge(catalog['direct'], infodirect['Departure'], infodirect['Destination'])
    
def components(catalog):
    catalog['components']= scc.KosarajuSCC(catalog['connections'])
        


# Funciones para creacion de datos

# Funciones de consulta
def cargaDatos(catalog):
    NumStops= gr.numVertices(catalog['connections'])
    NumRutes= gr.numEdges(catalog['connections'])
    NumCities= lt.size(mp.keySet(catalog['cities']))


    return NumStops,NumRutes, NumCities,catalog['prim_pos'],catalog['ult_pos']

# Funciones utilizadas para comparar elementos dentro de una lista
def requerimiento1(catalog):
    lista=lt.newList()
    llaves=mp.keySet(catalog['stops'])
    it1=it.newIterator(llaves)
    while it.hasNext(it1):
        elemento=it.next(it1)
        if lt.size(gr.adjacents(catalog['connections'], elemento)) > 1:
            numsalidas=lt.size(mp.get(catalog['rutes'], elemento)['value'])
            numentradas=lt.size(mp.get(catalog['exitrutes'], elemento)['value'])
            entrada= mp.get(catalog['stops'], elemento)['value']
            total=numsalidas + numentradas
            infototal= [entrada, total, numentradas, numsalidas ]
            lt.addLast(lista, infototal)
    return lista

def requerimiento2(catalog, iata1, iata2):
    catalog['components']= scc.KosarajuSCC(catalog['connections'])
    conectados= scc.stronglyConnected(catalog['components'],iata1, iata2 )
    total= scc.connectedComponents(catalog['components'])
    resp= ''
    if conectados == True:
        resp='Estan en el mismo cluster'
    else:
        resp='ANS= False'

def requerimiento3(catalog, ciudadA, ciudadB):
    infociudadA= mp.get(catalog['cities'], ciudadA)['value']
    infociudadB= mp.get(catalog['cities'], ciudadB)['value']
    aeropuertoA=None
    aeropuertoB=None
    disA=20
    disB=20
    llaves=mp.keySet(catalog['stops'])
    it1=it.newIterator(llaves)
    while it.hasNext(it1):
        elemento=it.next(it1)
        infoar=mp.get(catalog['stops'], elemento)['value']
        v1= haversine( float(infoar['Longitude']), float(infoar['Latitude']), float(infociudadA['lng']),float(infociudadA['lat']))
        v2= haversine( float(infoar['Longitude']), float(infoar['Latitude']), float(infociudadB['lng']),float(infociudadB['lat']))
        if  v1 <= disA:
            aeropuertoA = elemento
            disA= v1
        if  v2 <= disB:
            aeropuertoB = elemento
            disB= v2
    if((aeropuertoA is not None ) and (aeropuertoB is not None)):
        Dijkstra=djk.Dijkstra(catalog['connections'], aeropuertoA)
        Pila= djk.pathTo(Dijkstra, aeropuertoB)
        distancia= djk.distTo(Dijkstra, aeropuertoB )
        return aeropuertoA, aeropuertoB, disA, disB, Pila, distancia


def requerimiento4(catalog,ciudad_origen, millas):
    infociudadA= mp.get(catalog['cities'], ciudad_origen)['value']
    disA=20
    aeropuertoA=''
    rta=None
    llaves=mp.keySet(catalog['stops'])
    it1=it.newIterator(llaves)
    while it.hasNext(it1):
        elemento=it.next(it1)
        infoar=mp.get(catalog['stops'], elemento)['value']
        v1= haversine(float(infoar['Longitude']), float(infoar['Latitude']), float(infociudadA['lng']),float(infociudadA['lat']))
        if  v1 < disA:
            aeropuertoA= elemento
            disA= v1
    km=float(millas)*1.60
    rutaExpansionMinima= pr.PrimMST(catalog['connections'])
    rutaExp= pr.prim(catalog['connections'], rutaExpansionMinima, aeropuertoA)
    ObtenerPeso= pr.weightMST(catalog['connections'], rutaExp)
    ruta= rutaExp['mst']
    millasNecesarias= (ObtenerPeso - km)/(1.6)
    return ruta, ObtenerPeso, millasNecesarias

def requerimiento5(catalog, aeropuerto):
    a1= mp.get(catalog['rutes'], aeropuerto)['value']
    lista1= lt.newList()
    lista2= lt.newList()
    it1=it.newIterator(a1)
    while it.hasNext(it1):
        elemento=it.next(it1)
        if lt.isPresent(lista1, elemento['Destination']) == 0:
            lt.addLast(lista1, elemento['Destination'])
            lt.addLast(lista2,elemento)

    return lista2
access_token = ""

def requerimiento6(catalog, origen, destino):
    
    headers = {"Authorization": "Bearer " + access_token}
    infoOrigen= me.getValue(mp.get(catalog['cities'], origen))
    infoDest = me.getValue(mp.get(catalog['cities'], destino))
    params = {
        "latitude": float(infoOrigen['lat']),
        "longitude": float(infoOrigen['lng']),
        "sort" : "relevance",
        "page[limit]" : 1
    }
    params2 = {
        "latitude": float(infoDest['lat']),
        "longitude": float(infoDest['lng']),
        "sort" : "relevance",
        "page[limit]" : 1
    }
    r = requests.get('https://test.api.amadeus.com/v1/reference-data/locations/airports', headers=headers, params=params)
    r2 = requests.get('https://test.api.amadeus.com/v1/reference-data/locations/airports', headers=headers, params=params2)
    
    aeroOri,aeroOriLat,aeroOriLng =  r.json()['data'][0]['iataCode'],float(r.json()['data'][0]['geoCode']["latitude"]),float(r.json()['data'][0]['geoCode']["longitude"])

    aeroDest,aeroDestLat,aeroDestLng = r2.json()['data'][0]['iataCode'],float(r2.json()['data'][0]['geoCode']["latitude"]),float(r2.json()['data'][0]['geoCode']["longitude"])
  
    Dijkstra=djk.Dijkstra(catalog['connections'], aeroOri)
    Pila= djk.pathTo(Dijkstra, aeroDest)
    distancia= djk.distTo(Dijkstra, aeroDest )
    
    disOri = haversine(float(infoOrigen['lng']),float(infoOrigen['lat']),float(aeroOriLng),float(aeroOriLat))
    disDest = haversine(float(infoDest['lng']),float(infoDest['lat']),float(aeroDestLng),float(aeroDestLat))
    return Pila,(distancia+disOri+disDest)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    formula tomada de https://stackoverflow.com/questions/42686300/how-to-check-if-coordinate-inside-certain-area-python
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


# Funciones de ordenamiento
def compareStops(p1, p2):
    stops= p2['key']
    if stops == p1:
        return 0
    elif p1 > stops:
        return 1
    else:
        return -1
def compareRutes(p1, p2):
    if p1 == p2:
        return 0
    else:
        return -1

def compareCities(p1, p2):
    sp2= p2['key']
    if p1 == sp2:
        return 0
    elif p1 > sp2:
        return 1
    else:
        return -1
