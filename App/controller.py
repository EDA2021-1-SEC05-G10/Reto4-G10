﻿"""
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
 """

import config as cf
import model
import csv


def init():
    analyzer = model.newCatalog()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadServices(analyzer):
    servicesfile = cf.data_dir + 'airports-utf8-small.csv'
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        model.add_stops(service, analyzer)
    return analyzer

def loadRutes(analyzer):
    servicesfile = cf.data_dir + 'routes-utf8-small.csv'
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        model.add_rutes(service, analyzer)
        model.add_exit_rutes(service, analyzer)
    return analyzer

def loadCities(analyzer):
    servicesfile = cf.data_dir + 'worldcities-utf8.csv'
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        model.add_cities(service, analyzer)
    return analyzer

def loadGraph(analyzer):
    model.components(analyzer)
    servicesfile = cf.data_dir + 'routes-utf8-small.csv'
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        model.add_graph(service, analyzer)
    return analyzer

# Inicialización del Catálogo de libros
def requerimiento1(catalog):
    return model.requerimiento1(catalog)

def requerimiento2(catalog, iata1, iata2):
    return model.requerimiento2(catalog, iata1, iata2)

def requerimiento3(catalog, ciudadA, ciudadB):
    return model.requerimiento3(catalog, ciudadA, ciudadB)

def requerimiento4(catalog,ciudad_origen, millas):
    return model.requerimiento4(catalog,ciudad_origen, millas)

def requerimiento5(catalog, aeropuerto):
    return model.requerimiento5(catalog, aeropuerto)

def requerimiento6(catalog, origen, destino):
    return model.requerimiento6(catalog,origen, destino)

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def loadDatos(analyzer):
    return model.cargaDatos(analyzer)
