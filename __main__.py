# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 15:36:50 2021

@author: angel
"""

from web_scraping_html import Pagina_segunda_mano
from web_scraping_auto import Searcher
from web_scraping_gsheet import GSheet
from time import sleep, time, strftime
import threading
import pywhatkit

def main(delegacion, tipo_inmueble, datos_urls_buscados):
    urls_encontrados = False
    
    print('\t* * * * * {}s en {} * * * * *'.format(tipo_inmueble,delegacion.title()))

    precios = [i*500000 for i in range(1,14)]
    
    for precio in precios:
        try:
            precio_menor = precio + 1
            if precio != precios[-1]:
                precio_mayor = precio + 500000
            else:
                precio_mayor = 0
                
            #print('\n--->',precio_menor, precio_mayor)
            
            buffer_datos_local = {'delegacion':delegacion, 'rango':[precio_menor, precio_mayor], 'datos':[]}
                
            ### Creamos una instancia de la clase Pagina_segunda_mano
            pagina = Pagina_segunda_mano()
            
            ### Obtenemos la raiz con características generales (ubicacion geográfica)
            pagina.generar_pagina(
                ciudad = 'cdmx',
                delegacion = delegacion,
                tipo = 'venta',
                inmueble = tipo_inmueble)
            
            ### Agregamos características específicas de la vivienda
            pagina.add_specs(
                banos = 0,
                habitaciones = 0,
                estacionamiento = 0,
                orden = 'date',
                precio_menor = precio_menor,
                precio_mayor = precio_mayor)
            
            ### Obtenemos urls de publicaciones nuevas con las características solicitadas
            urls = pagina.get_urls_publicaciones()
            
            ### Si obtenemos publicaciones nuevas con las características deseadas, procedemos a buscar información
            if len(urls) > 0:
                ### Filtramos los datos por url que ya fueron buscados
                urls = list(filter(lambda url : not(url in datos_urls_buscados), urls))
                if len(urls) > 0:
                    if urls_encontrados == False:
                        urls_encontrados = True
                        searcher = Searcher()
                        searcher.iniciar_sesion_segunda_mano()
                    ### Buscar datos en cada url
                    datos = searcher.buscar_datos(urls)
                    buffer_datos_local['datos'] = datos
                    lock.acquire()
                    buffer_datos.append(buffer_datos_local)
                    lock.release()
            sleep(1)
        except Exception as e:
            print('Hubo un error.', e)
            
    if urls_encontrados == True:
        searcher.cerrar_ventana()

if __name__ == '__main__':
    delegaciones = ['benito_juarez', 'iztacalco', 'cuauhtemoc', 'coyoacan', 'azcapotzalco', 'alvaro_obregon', 'cuajimalpa_de_morelos', 'gustavo_a_madero', 'iztapalapa', 'la_magdalena_contreras', 'miguel_hidalgo', 'milpa_alta', 'tlahuac', 'tlalpan', 'venustiano_carranza', 'xochimilco']
    delegaciones = delegaciones[:]
    num_delegaciones = len(delegaciones)
    #tipos_arrendamiento = ['venta', 'renta']
    tipos_arrendamiento = ['venta']
    #tipos_inmueble = ['departamento','casa']
    tipos_inmueble = ['departamento']
    
    google_sheets = {'C21_web_scraping':'https://docs.google.com/spreadsheets/d/1w-qQXqbejVOz08PE1kY7QqVTO0UMi0CmL6zs9mDbeeE'}

    buffer_datos = []
    
    count_datos = 0
    
    lock=threading.Lock()
    
    t0 = time()
    
    sheet = GSheet()
    sheet.conectar_con_sheet(google_sheets['C21_web_scraping'])
    
    
    threads = []
    for i in range(4):
        primeras_delegaciones = delegaciones.pop(0)
        sheet.conectar_con_worksheet(primeras_delegaciones)
        thread = threading.Thread(target = main, kwargs = {'delegacion':primeras_delegaciones, 'tipo_inmueble':'departamento', 'datos_urls_buscados':sheet.urls_en_database})
        thread.start()
        threads.append(thread)
    
    while True:
        lock.acquire()
        if len(delegaciones) < 1 and len(buffer_datos)<1 and not(True in list(map(lambda thread : thread.is_alive(),threads))):
            lock.release()
            break
        elif len(delegaciones) > 0 and False in list(map(lambda thread : thread.is_alive(),threads)):
            thread_disponible = list(filter(lambda thread : not thread.is_alive(),threads))[0]
            thread_nuevo = threading.Thread(target = main, kwargs = {'delegacion':delegaciones.pop(0), 'tipo_inmueble':'departamento', 'datos_urls_buscados':[]})
            threads[threads.index(thread_disponible)] = thread_nuevo
            thread_nuevo.start()
            #print('---> Threads:', threads)
        if len(buffer_datos) > 0:
            datos_input = buffer_datos.pop(0)
            sheet.conectar_con_worksheet(datos_input['delegacion'])
            sheet.actualizar_worksheet(rango=datos_input['rango'], append = datos_input['datos'])
            count_datos = count_datos + len(datos_input['datos'])
        else:
            print('Loading....')
        lock.release()
        sleep(3)
    
    """
    
    """
    
    for thread in threads:
        thread.join()
    
    tf = time()
    
    tiempo_total = tf - t0
    
    print('El programa tardó {} minutos {} segundos'.format(tiempo_total//60, tiempo_total - tiempo_total//60*60))
    print('Se recopilaron {} datos en {} delegaciones.'.format(count_datos, num_delegaciones))
    
    pywhatkit.sendwhatmsg_instantly('+5215554601830', 'Programa: Ya acabé xd\n{}'.format(strftime('%d/%m/%y ; %H:%M:%S')))
    