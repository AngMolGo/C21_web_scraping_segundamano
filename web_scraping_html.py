# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 15:37:02 2021

@author: angel
"""

from bs4 import BeautifulSoup as bs
import requests
import csv

class Pagina_segunda_mano():
    def __init__(self):
        self.url = 'https://www.segundamano.mx'
        self.urls_publicaciones = []

    def generar_pagina(self, delegacion, ciudad='cdmx', tipo = 'venta', inmueble = 'departamento'):
        raiz = 'https://www.segundamano.mx/anuncios'
        ciudades = {'cdmx':'ciudad-de-mexico', 'ciudad_de_mexico':'ciudad-de-mexico'}
        delegaciones = {'benito_juarez':'benito-juarez', 'iztacalco':'iztacalco', 'azcapotzalco':'azcapotzalco', 'cuauhtemoc':'cuauhtemoc','coyoacan':'coyoacan', 'alvaro_obregon' : 'alvaro-obregon', 'cuajimalpa_de_morelos' : 'cuajimalpa-de-morelos', 'gustavo_a_madero':'gustavo-a-madero', 'iztapalapa':'iztapalapa', 'la_magdalena_contreras' : 'la-magdalena-contreras', 'miguel_hidalgo':'miguel-hidalgo', 'milpa_alta':'milpa-alta', 'tlahuac':'tlahuac', 'tlalpan':'tlalpan', 'venustiano_carranza':'venustiano-carranza', 'xochimilco':'xochimilco'}
        tipo_ = {'venta':'venta-inmuebles','renta':'renta-inmuebles'}
        inmuebles = {'departamento':'departamentos', 'casa':'casas'}
        self.url = '/'.join([raiz, ciudades[ciudad.lower()], delegaciones[delegacion.lower()], tipo_[tipo.lower()], inmuebles[inmueble.lower()]])
    
    def add_specs(self, banos = 0, habitaciones = 0, estacionamiento = 0, orden = '', precio_menor = 0, precio_mayor = 100000000):
        especificaciones = {'banos' : banos, 'estacionamiento' : estacionamiento, 'habitaciones' : habitaciones, 'orden' : orden, 'precio' : '{}-{}'.format(precio_menor, precio_mayor)}
        especificaciones_ = []
        for especificacion in especificaciones:
          if especificaciones[especificacion] != 0 and especificaciones[especificacion] != '':
            if especificacion == 'precio':
                if (precio_menor < 0 or precio_mayor < 0):
                    continue
                elif precio_menor*precio_mayor == 0 and not(precio_mayor == precio_menor):
                    if precio_mayor == 0:
                        precio_mayor = ''
                    elif precio_menor == 0:
                        precio_menor = ''
                    especificaciones['precio'] = '{}-{}'.format(precio_menor, precio_mayor)
                    especificaciones_.append('{}={}'.format(especificacion,especificaciones[especificacion]))
                    continue
                elif precio_mayor - precio_menor <= 0:
                    continue
            elif type(especificaciones[especificacion]) == int and especificacion != 'habitaciones':
              especificaciones[especificacion] += 1
            especificaciones_.append('{}={}'.format(especificacion,especificaciones[especificacion]))
        self.url += '?inmobiliaria=0&'+'&'.join(especificaciones_)
        #print('Se agregaron características a la busqueda')
    
    def get_urls_publicaciones(self):
        try:
            pagina = self.url
            num_pagina = 1
            urls_encontradas = 0
            with open('urls_ya_buscadas.csv', 'r') as File:
                urls_ya_buscadas = csv.reader(File)
                urls_ya_buscadas_ = []
                for url in urls_ya_buscadas:
                    if url != []:
                        urls_ya_buscadas_.append(url[0])
                urls_ya_buscadas = urls_ya_buscadas_
                #print('urls:',urls_ya_buscadas)
                while True:
                    ### Algo que se estudia en la página
                    req = requests.get(pagina + '&pagina={}'.format(num_pagina))
                    soup = bs(req.content, 'html.parser')
                    
                    hijo = soup.find('script', {'type':'application/ld+json'})
                    hijo = str(list(hijo)[0])
                    hijo = hijo[3:len(hijo)-3]
                    hijo = eval(hijo)
                    hijo = hijo['itemListElement']
                    
                    if len(hijo) > 0:
                        for i in hijo:
                            url = i['item']['url']
                            if url not in self.urls_publicaciones and url not in urls_ya_buscadas:
                                self.urls_publicaciones.append(url)
                                #print(urls_encontradas)
                                urls_encontradas += 1
                        num_pagina += 1
                    else:
                        if urls_encontradas > 0:
                            #print('Se encontraron {} nuevas publicaciones en {} páginas.'.format(urls_encontradas, num_pagina - 1))
                            pass
                        else:
                            #print('No se encontraron publicaciones nuevas')
                            pass
                        break
            return self.urls_publicaciones
            
        except Exception as e:
            print('Hubo un error, contacte con el administrador.\nError: ', e)