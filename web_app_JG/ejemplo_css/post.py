#!/usr/bin/env python
'''
API Monitor cardíaco
---------------------------
Autor: Inove Coding School
Version: 1.0
 
Descripcion:
Se utiliza request para generar un HTTP post al servidor Flask
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inovecode.com"
__version__ = "1.0"

import os
import requests

from config import config

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
server = config('server', config_path_name)

ip = server['host']
port = server['port']
endpoint = 'registro'

url = f'http://{ip}:{port}/{endpoint}'

if __name__ == "__main__":
    try:
        id_number = str(input('Ingrese el numero de caravana:'))
        peso = int(input('Ingrese el peso:'))
        farm = str(input('Ingrse el nombre del establecimiento:'))
        category = str(input('Ingrese la categoria del animal:'))
        post_data = {"id_number": id_number, "farm": farm, "category": category, "live_weight": peso}        
        x = requests.post(url, data = post_data)
        print('POST enviado a:',url)
        print('Datos:')
        print(post_data)
    except:
        print('Error, POST no efectuado')