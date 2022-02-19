# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 14:19:20 2022

@author: angel
"""

import gspread
import pandas as pd
import time
import gspread.utils
import csv

class GSheet():
    def __init__(self):    
        self.vincular_cuenta()
            
    ### Se conecta con la cuenta robot, si no se puede conectar, el programa ya no continua
    def vincular_cuenta(self):
        try:
            self.gc = gspread.service_account()
            print('Se vinculó a la cuenta con satisfacción')
        except Exception as e:
            print('Ocurrió un error. Comuniquece con el administrador.', e)
    ### LISTO
    
    ### Se conecta con la hoja de datos de Google, en el worksheet correcto
    def conectar_con_sheet(self, sheet_url):
        try:
            ### Sheet
            self.sh = self.gc.open_by_url(sheet_url)
            self.worksheets_list = [ works.title for works in self.sh.worksheets()]
            #print('worksheet_lists: ',self.worksheets_list)
            self.ranges_name_list = [range_['name'] for range_ in self.sh.list_named_ranges()]
            #print('range_lists: ',self.ranges_name_list)
            
            #print('Se conectó a la hoja de datos')
            
        except Exception as e:
            print('Ocurrió un error. Comuniquece con el administrador.', e)
    ### CREO QUE YA ESTÁ LISTO
    
    def conectar_con_worksheet(self, worksheet_name):
        try:
            if worksheet_name in self.worksheets_list:
                self.worksheet = self.sh.worksheet(worksheet_name)
                #print('\n\nSe conectó al worksheet {}'.format(self.worksheet.title))
                ### Por si luego lo utilizo
                self.urls_en_database = self.worksheet.col_values(6)[3:]
                #print('urls en worksheet: ',self.urls_en_database)
            else:
                print('No existe un worksheet de esa delegación. Comuníquese con el administrador.')
                
        except Exception as e:
            print('Ocurrió un error. Comuniquece con el administrador.', e)
            
            
            
    def ad_in_worksheet(self, url):
        try:
            if url in self.urls_en_database:
                return True
            else:
                return False
            
        except Exception as e:
            print('Ocurrió un error. Comuniquece con el administrador.', e)
            
    def actualizar_worksheet(self, rango, append = []):
        try:
            buscados = []
            for url in append:
                buscados.append([url[5]])
            
            if len(append) > 0:
                #print('Hola mundo')
                num_rows = self.worksheet.row_count
                #print(num_rows)
                
                range_name = '{}_{}_{}'.format(self.worksheet.title, rango[0], rango[1])
                if range_name not in self.ranges_name_list:
                    append = [[range_name]+['-']*(len(append[0])-1)] + append
                    #print('preparate')
                    inserted_rows = self.worksheet.insert_rows(append, row=num_rows)
                    #print(appended_rows)
                    self.worksheet.define_named_range(inserted_rows['updates']['updatedRange'].split('!')[-1], range_name)
                else:
                    range_ = self.worksheet.range(name = range_name)
                    #print('Range_',range_)
                    range_first_cell = range_[0]
                    #print(range_first_cell)
                    ####range_last_cell = range_[-1]
                    #print(range_last_cell)
                    
                    data = append
                    
                    #####range_name_complete_info = list(filter(lambda x : True if x['name'] == range_name else False, self.sh.list_named_ranges()))[0]
                    #print(range_name_complete_info)
                    
                    #####self.worksheet.delete_named_range(range_name_complete_info['namedRangeId'])
                    #####inserted_rows = self.worksheet.insert_rows(values = data, row=range_last_cell.row + 1)
                    inserted_rows = self.worksheet.insert_rows(values = data, row=range_first_cell.row + 1)
                    #print(inserted_rows)
                    #print(range_first_cell.address)
                    #print(inserted_rows['updates']['updatedRange'].split(':')[-1])
                    #####self.worksheet.define_named_range(name = '{}:{}'.format(range_first_cell.address, inserted_rows['updates']['updatedRange'].split(':')[-1]), range_name = range_name)
            tiempo = time.strftime('%d/%m/%y ; %H:%M:%S')
            self.worksheet.update_acell('B1', tiempo)
            with open('urls_ya_buscadas.csv', 'a') as File:
                writer = csv.writer(File, delimiter =',')
                writer.writerows(buscados)
            #print(tiempo)
        except Exception as e:
            print('Ocurrió un error. Comuniquece con el administrador.', e)
         