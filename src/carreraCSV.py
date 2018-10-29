'''
Created on 22 oct. 2018

@author: apavond
'''

import os
import requests
import csv
import argparse
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

url='https://imd.sevilla.org/app/carreras/clasificaciones_carrera.php'
id='general'
idcarrera='19D1A60F-A110-4C4B-B4D8-56755CB1F5BC'
headers={}
formData={}

formData['id']=id
formData['idcarrera']=idcarrera

headers['Content-Type']='application/x-www-form-urlencoded'
headers['Origin']='https://imd.sevilla.org'

def llamadaImd(formData, headers, listaCorredores, url = 'https://imd.sevilla.org/app/carreras/clasificaciones_carrera.php'):
    response=requests.post(url, data = formData, headers = headers)
    soup=BeautifulSoup(response.text, 'html.parser')
    nombreCarrera=soup.find('h2').find(text=True)
    esCabecera=True
    listado=soup.find('table')
    listResponse=listado.findAll('tr')
    for corredor in listResponse:
        if(esCabecera):
            camposCabecera=corredor.findAll('th')
            cabecera=[camposCabecera[0].find(text=True),camposCabecera[1].find(text=True),camposCabecera[2].find(text=True),camposCabecera[3].find(text=True),camposCabecera[4].find(text=True),camposCabecera[5].find(text=True),camposCabecera[6].find(text=True),camposCabecera[7].find(text=True)]
            listaCorredores.append(cabecera)
            esCabecera=False
        else:
            camposCorredor=corredor.findAll('td')
            if len(camposCorredor)==8:
                corredorAdd=[camposCorredor[0].find(text=True),camposCorredor[1].find(text=True),camposCorredor[2].find(text=True),camposCorredor[3].find(text=True),camposCorredor[4].find(text=True),camposCorredor[5].find(text=True),camposCorredor[6].find(text=True),camposCorredor[7].find(text=True)]
                listaCorredores.append(corredorAdd)
    return nombreCarrera


response=[]

nombreArchivo=llamadaImd(formData, headers, response)

currentDir = os.path.dirname(__file__)
filePath = os.path.join(currentDir, nombreArchivo+'.csv')

with open(filePath, 'w', newline='') as csvFile:
  writer = csv.writer(csvFile)
  for corredor in response:
    writer.writerow(corredor)
