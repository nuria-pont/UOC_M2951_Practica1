# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 19:37:27 2020

@author: ricard
"""

import os
import requests
import csv
import argparse
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def obtenirResultats(numResultatsPerProva, numTemporades=-1):
    fd={
    'salida_web': '1',
    'crono': 'P',
    'viento_activo': '1',
    'cod_viento': '1',
    'desglose': '0',
    'var_relevistas': '0',
    'fecha_o_temporada': 't',
    'nacionalidad': '1',
    'var_desglose': '1',
    'tipo_lista_seguimiento': '-1',
    'codigo_licencia': '',
    'bpublish': '1',
    'bevent': '0',
    'nombre_dele': '',
    'sex': 'M',
    'tip': 'AL',
    'categorias': '',
    'GENDERCODE': '',
    'EVENTCODE': '',
    'EVENTPARENTCODE': '',
    'EVENTTYPE': '',
    'EVENTSUBTYPE': '',
    'STYLE': '',
    'DESCR': '',
    'cod_unidad_medida': '',
    'MAXWIND': '',
    'MAXRESULT': '', 
    'ATHLETEINDEX': '', 
    'CHRONOTYPE': '',
    'tope_cabecera': '',
    'elecmanual': '',
    'TOP': numResultatsPerProva,
    'marcas': '1',
    'federaciones': '', 
    'cod_temporada': '20',
    'cod_categoria': 'AB',
    'sector': '-1',
    'prueba': '-1',
    'cod_federacion': '-1',
    'club': '-1',
            }
    
    pag=requests.get("https://www.rfea.es/web/estadisticas/ranking.asp")
    soup = BeautifulSoup(pag.content)
    s=soup.find('select', id="cod_temporada")
    
    temporades=[]
    for e in s.find_all('option'):
        if numTemporades==0:
            break
        temporades.append(e['value'])
        numTemporades-=1
    
    generes=['M','F']
    
    tipus=['AL','PC','RT']
    
    j=0
    a=[]
    for temp in temporades:
        print(temp)
        fd['cod_temporada']=temp
        for gen in generes:
            print(gen)
            fd['sex']=gen
            for tip in tipus:
                print(tip)
                fd['tip']=tip
                #page = requests.post("https://www.rfea.es/web/estadisticas/rankingResults.asp",headers=post_headers,data=fd)#.text
                page = requests.post("https://www.rfea.es/web/estadisticas/rankingResults.asp",data=fd)#.text
                page.encoding = 'utf-8'
                page=page.text
                sp = BeautifulSoup(page, "lxml")
                
                taules=sp.find_all('table')
                h2s=sp.find_all('h2')
                i=0
                s=""
                
                
                for taula in taules[1:]:
                    files=taula.find_all('tr')
                    while h2s[i].next_sibling.next_sibling.name!='table':
                        i+=1
                    if i>=0 and i<len(h2s)-1 and len(files)>0:
                        if not h2s[i].text[0:6]=="Viento":
                            l=0
                            for fila in files:
                                if len(fila.find_all('b'))<=0:
                                    continue
                                if h2s[i].text.find('lón')>0 and l%2==1:
                                    l+=1
                                    continue
                                a.append([])
                                a[j].append(tip)
                                a[j].append(gen)
                                a[j].append(h2s[i].text)
                                k=0
                                for columna in fila.find_all('b'):
                                    if k==2 and not is_number(columna.text) and not columna.text=='':
                                        a[j].append('')
                                    a[j].append(columna.text)
                                    k+=1
                                    
                                j+=1
                                l+=1
                        i+=1
    return a



b=obtenirResultats(2000,5)
for i in range(30):
    print(b[i])
print(b[0])
print(b[1])
"1,5".isdecimal()


resultat_per_treballar=b

with open('resultats.csv','w', encoding="utf-8",newline='') as file:
               c1= 'Pista Cubierta(PC) Aire Libre(AL) Ruta_Marcha(RT)'
               c2='sexo'
               c3='Descripción'
               c4='RK'
               c5='Marca'
               c6='Viento'
               c7='Atleta'
               c8='F.Nacimiento'
               c9='CA'
               c10='n.Licencia'
               c11='Federacion'
               c12='Club'
               c13='Puesto'
               c14='Lugar'
               c15='Fecha'
               columnes_name = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15]
               writer=csv.writer(file,delimiter=';')
               writer.writerow(columnes_name)
               writer.writerows(resultat_per_treballar)
               
               

 






