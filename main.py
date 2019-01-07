

import click

# Local
from parserSchool import printInfoSchool, printInfoSchoolCSV, printInfoSchoolHTML, printInfoSchoolJSON
from scrap import getSchoolByCCT

@click.command()
@click.option('--cct', type=str, help='Especifica el cct de una escuela para obtener sus datos')
@click.option('--to-json', is_flag=True, help='Devuelve los datos en formato JSON')
@click.option('--to-html', is_flag=True, help='Devuelve los datos en una tabla HTML')
@click.option('--to-csv', is_flag=True, help='Devuelve los datos en formato csv')

def getInfoSchool(cct, to_json, to_html, to_csv):
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
                printInfoSchoolJSON(objectSchool)
            elif to_html:
                printInfoSchoolHTML(objectSchool)
            elif to_csv:
                printInfoSchoolCSV(objectSchool)
            else:
                printInfoSchool(objectSchool)

# INICIA PROGRAMA
if __name__ == '__main__':
    getInfoSchool()