""" Funciones creadas para parsear los datos en CSV, JSON, HTML"""

import sys
import csv
import json
# DEFINICION DE FUNCIONES
def printInfoSchoolJSON(objectSchool):
    print(json.dumps(objectSchool))


def printInfoSchool(objectSchool):
    for key, value in objectSchool.items():
        if key == 'direccion':
            for key2, value2 in value.items():
                print('{:12} {}'.format(key2, value2))
        else:
            print('{:12} {}'.format(key,value))


def printInfoSchoolCSV(objectSchool):
    cvs_out = csv.writer(sys.stdout)

    cvs_out.writerow([
        'Nombre',
        'Calle' ,
        'Municipio',
        'Localidad',
        'Entidad',
        'CCT',
        'Nivel',
        'Turno',
        'Tipo',
        'Teléfonos'
    ])


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