# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 15:36:50 2021

@author: angel
"""

from web_scraping_html import Pagina_segunda_mano
from web_scraping_auto import Searcher
from web_scraping_gsheet import GSheet
from time import sleep

delegaciones = ['benito juarez', 'iztacalco', 'cuauhtemoc', 'coyoacan', 'azcapotzalco', 'alvaro obregon', 'cuajimalpa de morelos', 'gustavo a madero', 'iztapalapa', 'la magdalena contreras', 'miguel hidalgo', 'milpa alta', 'tlahuac', 'tlalpan', 'venustiano carranza', 'xochimilco']
#delegaciones = ['iztacalco']
delegaciones = ['benito juarez', 'iztacalco']
tipos_arrendamiento = ['venta', 'renta']
tipos_inmueble = ['departamento']

google_sheets = {'C21_web_scraping':'https://docs.google.com/spreadsheets/d/1w-qQXqbejVOz08PE1kY7QqVTO0UMi0CmL6zs9mDbeeE'}

def main(**kwargs):
    ### Creamos una instancia de la clase Pagina_segunda_mano
    pagina = Pagina_segunda_mano()
    
    ### Obtenemos la raiz con características generales (ubicacion geográfica)
    pagina.generar_pagina(
        ciudad = 'cdmx',
        delegacion = kwargs['delegacion'],
        tipo = kwargs['tipo_arrendamiento'],
        inmueble = kwargs['tipo_inmueble'])
    
    ### Agregamos características específicas de la vivienda
    pagina.add_specs(
        banos = kwargs['banos'],
        habitaciones = kwargs['habitaciones'],
        estacionamiento = kwargs['estacionamiento'],
        orden = 'date',
        precio_menor = kwargs['precio_menor'],
        precio_mayor = kwargs['precio_mayor'])
    
    ### Obtenemos urls de publicaciones nuevas con las características solicitadas
    urls = pagina.get_urls_publicaciones()[:5]
    
    ### Si obtenemos publicaciones nuevas con las características deseadas, procedemos a buscar información
    if len(urls) > 0:
        ### Nos linkeamos a Google Sheets para filtrar los urls repetidos
        sheet = GSheet()
        sheet.vincular_cuenta()
        sheet.conectar_con_sheet(google_sheets['C21_web_scraping'],
                                 delegacion = kwargs['delegacion'],
                                 tipo_arrendamiento = kwargs['tipo_arrendamiento'],
                                 tipo_inmueble = kwargs['tipo_inmueble'])
        
        ### Filtramos los datos por url que ya fueron buscados
        urls = list(filter(lambda url : not sheet.ad_in_worksheet(url), urls))
    
        if len(urls) > 0:
            ### Creamos una instancia de la clase Searcher
            searcher = Searcher()
            
            ### Iniciamos sesión en segunda mano
            searcher.iniciar_sesion_segunda_mano()
            
            ### Buscar datos en cada url
            datos = searcher.buscar_datos(urls)
            
            ### Cerrar ventana
            searcher.cerrar_ventana()
            
            ### Filtramos los datos nuevamente
            data = list(filter(lambda dato : True, datos))
            
            ### Subir a Google Sheets
            sheet.actualizar_worksheet(append = data)

if __name__ == '__main__':
    for tipo_arrendamiento_ in tipos_arrendamiento:
        for tipo_inmueble_ in tipos_inmueble:
            for delegacion_ in delegaciones:
                
                print('\n\n\t* * * * * {} * * * * *'.format(delegacion_.title()))
                
                if tipo_arrendamiento_ == 'renta':
                    precio_menor_ = 0
                    precio_mayor_ = 0
                elif tipo_arrendamiento_ == 'venta':
                    precio_menor_ = 0
                    precio_mayor_ = 0
                    
                main(delegacion = delegacion_,
                     tipo_arrendamiento = tipo_arrendamiento_,
                     tipo_inmueble = tipo_inmueble_,
                     
                     habitaciones = 0,
                     banos = 0,
                     estacionamiento = 0,
                     precio_menor = precio_menor_,
                     precio_mayor = precio_mayor_)
                
                sleep(2)
                
    