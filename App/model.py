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
assert cf

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
                    'ult_pos': None
                    }

        analyzer['stops'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStops)
        analyzer['rutes'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareRutes)
        analyzer['cities'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareCities)
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStops)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo
def add_stops(infostop, catalog):
    info= mp.get(catalog['stops'], infostop['IATA'])
    if info is None:
        mp.put(catalog['stops'],infostop['IATA'],infostop)
        gr.insertVertex(catalog['connections'], infostop['IATA'])
        
def add_rutes(inforutes, catalog):
    info= mp.get(catalog['rutes'], inforutes['Departure'])
    if info is None:
        rutes= lt.newList('SINGLE_LINKED')
        lt.addLast(rutes, inforutes)
        mp.put(catalog['rutes'],inforutes['Departure'],rutes)
    else:
        lt.addLast(info['value'],inforutes)
    gr.addEdge(catalog['connections'], inforutes['Departure'], inforutes['Destination'], inforutes['distance_km'])

def add_cities(infocities, catalog):
    info= mp.get(catalog['cities'], infocities['city_ascii'])
    catalog['ult_pos']=infocities
    if info is None:
        mp.put(catalog['cities'],infocities['city_ascii'],infocities)
        


# Funciones para creacion de datos

# Funciones de consulta
def cargaDatos(catalog):
    NumStops= gr.numVertices(catalog['connections'])
    NumRutes= gr.numEdges(catalog['connections'])
    NumCities= lt.size(mp.keySet(catalog['cities']))
    Vertices= gr.vertices(catalog['connections'])
    print(Vertices['first'])
    Primerelement=Vertices['first']
    info= mp.get(catalog['cities'],Primerelement)['value']

    return NumStops,NumRutes, NumCities, info, catalog['ult_pos']

# Funciones utilizadas para comparar elementos dentro de una lista
def requerimiento1(catalog):
    lista=newList()
    llaves=mp.keySet(catalog['stops'])
    it1=it.newIterator(llaves)
    while it.hasNext(it1):
        elemento=it.next(it1)
        if lt.size(gr.adjacents(catalog['connections'], elemento)) > 1:
            entrada= mp.get(catalog['stops'], elemento)['value']
            lt.addLast(lista, entrada)
    return lista

def requerimiento2(catalog, iata1, iata2):
    catalog['components']= scc.KosarajuSCC(catalog['connections'])
    conectados= scc.stronglyConnected(catalog['components'],iata1, iata2 )
    total= scc.connectedComponents(catalog['components'])
    resp= ''
    if conectados == True:
        resp='Estan en el mismo cluster'
    else:
        resp='No estan en el mismo cluster'
    
    return resp, total

        

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
    if p1 == p2:
        return 0
    else:
        return -1

