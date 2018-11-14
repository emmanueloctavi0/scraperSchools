#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from requests import get, post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import click
import json

# DEFINICION DE CONSTANTES
DISTRITO_FEDERAL = 9
url_api = 'http://www.mejoratuescuela.org/api/escuelas/'
url = 'http://www.mejoratuescuela.org/escuelas/index/{}'

@click.command()
@click.option('--cct', type=str, help='Especifica el cct de una escuela para obtener sus datos')
@click.option('--to-json', is_flag=True, help='Devuelve los datos en formato JSON')
@click.option('--to-html', is_flag=True, help='Devuelve los datos en una table HTML')

def getInfoSchool(cct, to_json, to_html):
    '''
    Obten información básica de las escuelas de México
    '''
    
    if cct == None:
        print('Debería de obtener todas las escuelas?')
    else:
        objectSchool = getSchoolByCCT(cct)
        if objectSchool == None:
            print('Hubo un error')
        else:
            if to_json:
                print(json.dumps(objectSchool))
            elif to_html:
                printInfoSchoolHTML(objectSchool)
            else:
                printInfoSchool(objectSchool)

# DEFINICION DE FUNCIONES
def printInfoSchool(objectSchool):
    for key, value in objectSchool.items():
        if key == 'direccion':
            for key2, value2 in value.items():
                print('{:12} {}'.format(key2, value2))
        else:
            print('{:12} {}'.format(key,value))


def printInfoSchoolHTML(objectSchool):

    plantilla = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Escuelas</title>
    <style>
        td {{
            padding: 10px;
        }}
        th, td, table {{
            border: 1px solid black;
        }}
    </style>
</head>
<body>
    <table>
        <tr>
            <th>Nombre</th>
            <th>Calle</th>
            <th>Municipio</th>
            <th>Localidad</th>
            <th>Entidad</th>
            <th>CCT</th>
            <th>Nivel</th>
            <th>Turno</th>
            <th>Tipo</th>
            <th>Teléfonos</th>
        </tr>
        {}
    </table>
</body>
</html>
    """
    arrayValues = []
    for key, value in objectSchool.items():
        if key == 'direccion':
            for value2 in value.values():
                arrayValues.append(value2)
        else:
            arrayValues.append(value)

    tr = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
        arrayValues[0],
        arrayValues[1],
        arrayValues[2],
        arrayValues[3],
        arrayValues[4],
        arrayValues[5],
        arrayValues[6],
        arrayValues[7],
        arrayValues[8],
        arrayValues[9],
    )
    html = plantilla.format(tr)
    print(html)

def getSchoolByCCT(cct):
    global url
    
    try:
        with closing(get(url.format(cct), stream=True)) as resp:
            if is_good_response(resp):
                raw_html = resp.content
                html = BeautifulSoup(raw_html, 'html.parser')
                objectSchool = getInfoFromHtml(html)
                return objectSchool
            else:
                return None
                

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def getInfoFromTag(html):
    leaftlet = html.find('leaflet')
    ng_init = leaftlet['ng-init']
    print(ng_init)

def getInfoFromHtml(html):

    school = {}
    direccion = {}

    #School's Name
    school['nombre'] = html.find_all('h1')[0].string

    #School's Address
    address = html.select('.address li')
    for addre in address:
        if 'Calle' in addre.string:
            direccion['calle'] = addre.string[7:]
        elif 'Municipio' in addre.string:
            direccion['municipio'] = addre.string[11:]
        elif 'Localidad' in addre.string:
            direccion['localidad'] = addre.string[11:]
        elif 'Entidad' in addre.string:
            direccion['entidad'] = addre.string[9:]
        
    school['direccion'] = direccion

    #School's Data
    schoolData = html.select('.block.school-banner-form li')

    for item in schoolData:
        
        if 'Clave' in item.string:
            school['cct'] = item.string[7:]
        elif 'Nivel' in item.string:
            school['nivel'] = item.string[7:]
        elif 'Turno' in item.string:
            school['turno'] = item.string[7:]
        elif 'Privada' in item.string or 'Pública' in item.string:
            school['tipo'] = item.string
        elif 'Teléfonos' in item.string:
            school['telefonos'] = item.string[11:]
    
    #School's count students
    # students = html.select('.datos-counters-1 .h3-num-datos')
    # if len(students) > 0:
    #     school['alumnos'] = int(students[0].string)
    
    #School's count employes
    # employes = html.select('.datos-counters-2 .h3-num-datos')
    # if len(employes) > 0:
    #     school['trabajadores'] = int(employes[0].string)

    #School's count groups
    # groups = html.select('.datos-counters-3 .h3-num-datos')
    # if len(groups) > 0:    
    #     school['grupos'] = int(groups[0].string)

    return school

    
    
def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def getAllSchools(entidad):

    payload = {
        'entidad': entidad,
        'localidad': '',
        'municipio': '',
        'niveles': '22',
        'p': 1,
        'schoolStatus': -1,
        'sort': 'Nombre de la escuela',
        # 'term': 'jose vasconselos',
        'type_test': 'planea'
    }

    resp = post(url, json=payload)
    respJSON = resp.json()
    return respJSON['escuelas']

# INICIA PROGRAMA
if __name__ == '__main__':
    getInfoSchool()
    pass