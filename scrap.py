#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from requests import get, post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json

# CONSTANTES
url_api = 'http://www.mejoratuescuela.org/api/escuelas/'
url = 'http://www.mejoratuescuela.org/escuelas/index/{}'

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

    return school


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)