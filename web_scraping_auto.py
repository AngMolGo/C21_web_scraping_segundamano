# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 18:09:36 2021

@author: angel
"""

from selenium import webdriver
import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

class Searcher():
    def __init__(self):
        #drivers = [webdriver.Chrome,webdriver.Opera]
        try:
            try:
                self.driver = webdriver.Edge(r"msedgedriver.exe")
            except Exception as e:
                print(e)
                self.driver = webdriver.Chrome(r"chromedriver.exe")
            finally:
                self.driver.maximize_window()
                sleep(2)
                self.driver.get('https://www.segundamano.mx/')
        except:
            print("Hubo un error al momento de inicializar el webdriver")
        
    def iniciar_sesion_segunda_mano(self):
        ### Este método se tiene que actualizar cada cierto tiempo
        try:
            self.driver.get('https://www.segundamano.mx/')
            
            ingresar = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div.header-container > div > div.header-container_general-info > div > div:nth-child(2) > div')))
            ingresar.click()
            
            login_email = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, 'login-email')))
            login_email.send_keys('angmolgo@gmail.com')
            
            login_password = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, 'login-password')))
            login_password.send_keys('C21WebScraping')
            
            acceder = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login-button-submit > div > button')))
            acceder.click()
            
            sleep(4)
            #print('Se inició sesión')
        except:
            print('Hubo un error al iniciar sesión en segunda mano, contacte con el administrador.')
            
    def buscar_datos(self, urls):
        try:
            datos = []
            buscados = []
            for url in urls:
                datos_de_anuncio = {'ID':'',
                                    'ubicacion':'',
                                    'telefono':'',
                                    'descripcion':'',
                                    'publicado':'',
                                    'url':url,
                                    'input_date':'',
                                    'nombre_vendedor':'',
                                    'publicaciones_del_vendedor':'',
                                    'precio':'',
                                    'habitaciones':'',
                                    'banos':'',
                                    'estacionamiento':''}
                try:
                    self.driver.get(url)
                    #print('\n',url)
                    
                    try:
                        telefono = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#av-Sidebar > div.av-AdReplay > div > div.av-AdReply_UserData > div.phoneContainer > div > span')))
                    except:
                        #print('No existe telefono\n\n')
                        buscados.append([url])
                        continue
                    
                    try:
                        descripciones = {}
                        descripciones_ = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div > div.sw-content-wrapper > div.av-AdviewContainer > div:nth-child(3) > div > div.av-Ad-Container-characteristics-container')))
                        descripciones_children = descripciones_.find_elements_by_tag_name('span')
                        for num_child in range(0,len(descripciones_children),2):
                            categoria = descripciones_children[num_child].text[:-1]
                            valor = descripciones_children[num_child + 1].text
                            descripciones[categoria] = valor
                        #print(descripciones)
                    except:
                        print('Hubo un error al buscar la información completa')
                    
                    descripcion = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ad-description > p')))
                    
                    try:
                        datos_de_anuncio['ubicacion'] = descripciones['Ubicación']
                    except:
                        pass
                    try:
                        datos_de_anuncio['habitaciones'] = descripciones['Habitaciones']
                    except:
                        pass
                    try:
                        datos_de_anuncio['estacionamiento'] = descripciones['Estacionamiento']
                    except:
                        pass
                    try:
                        datos_de_anuncio['banos'] = descripciones['Baños']
                    except:
                        pass
                    try:
                        datos_de_anuncio['publicado'] = descripciones['Publicado']
                    except:
                        pass
                    
                    ID = url.split('-')[-1]
                    datos_de_anuncio['ID'] = ID
                    #print('ID: ', ID)
                    
                    telefono =str(telefono.text)
                    #print('Teléfono:', telefono)
                    datos_de_anuncio['telefono'] = telefono

                    descripcion =str(descripcion.text).replace('\n','')
                    #print('Descripción:', descripcion)
                    datos_de_anuncio['descripcion'] = descripcion
                    
                    try:
                        try:
                            precio = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#av-Sidebar > div.av-AdSummary > div > div.summaryInfo > div > span.av-AdPrice')))
                        except:
                            precio = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#av-Sidebar > div.av-AdSummary > div > div.summaryInfo > div > span.av-AdPrice.price-dop')))
                        precio = str(precio.text)
                        datos_de_anuncio['precio'] = precio
                    except:
                        pass
                    
                    datos_de_anuncio['input_date'] = time.strftime('%d/%m/%y')
                    
                    try:
                        seccion = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#av-Sidebar > div.av-AdReplay > div > div.av-AdReply_UserData > div.av-AdReply_UserData-txt')))
                        ver_mas = seccion.find_element_by_tag_name('a')
                        
                        ver_mas.click()
                        
                        name = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div.ma-main_ContainerProfile > div > div > div.profile-info > div.profile-info-personal > div.user > div.name')))
                        str_name = str(name.text)
                        if str_name == '' or str_name == ' ':
                            sleep(1)
                            name = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div.ma-main_ContainerProfile > div > div > div.profile-info > div.profile-info-personal > div.user > div.name')))
                            str_name = str(name.text)
                        #print('Nombre:', str_name)
                        datos_de_anuncio['nombre_vendedor'] = str_name
                        num_publicaciones =  WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div.ma-main_ContainerProfile > div > div > div.profile-ads > p')))
                        str_num = str(num_publicaciones.text).split()[0]
                        if int(str_num) < 1:
                            sleep(1)
                            num_publicaciones =  WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div.ma-main_ContainerProfile > div > div > div.profile-ads > p')))
                            str_num = str(num_publicaciones.text).split()[0]
                        #print('Número de publicaciones:', str_num)
                        datos_de_anuncio['publicaciones_del_vendedor'] = str_num
                    except:
                        print('No se pudo leer algún dato del vendedor')
                    
                    datos.append(list(datos_de_anuncio.values()))
                    #print('\n\n')
                    ##av-Sidebar > div.av-AdReplay > div > div.av-AdReply_UserData > div.av-AdReply_UserData-txt > div.adTypeLabel > a
                    ### Ya que obtuvo los datos, escribimos la url en nuestro archivo de urls ya buscadas
                except Exception as e:
                    print('Hubo un error :(', e)
            with open('urls_ya_buscadas.csv', 'a') as File:
                writer = csv.writer(File, delimiter =',')
                writer.writerows(buscados)
            return datos
        except:
            print('Hubo un error, contacte con el administrador.')
        
    def cerrar_ventana(self):
        self.driver.close()