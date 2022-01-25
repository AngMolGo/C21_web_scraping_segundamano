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
        pass
            
    def vincular_cuenta(self):
        try:
            self.gc = gspread.service_account()
            print('Se vinculó a la cuenta con satisfacción')
        except Exception as e:
            print('Ocurrió un error. Comuniquece con el administrador.', e)
    
    def conectar_con_sheet(self, sheet, delegacion, tipo_arrendamiento, tipo_inmueble):
        self.tipo_arrendamiento, self.tipo_inmueble = [tipo_arrendamiento, tipo_inmueble]
        try:
            self.sh = self.gc.open_by_url(str(sheet))
            self.worksheet = self.sh.worksheet('{}_{}'.format(tipo_arrendamiento, tipo_inmueble))
            self.ranges_name = self.sh.list_named_ranges()
            self.delegacion_name = delegacion.replace(' ','_')
            self.range_name = "{}_{}_{}".format(self.delegacion_name,tipo_arrendamiento, tipo_inmueble)
            self.df = pd.DataFrame(self.worksheet.get_values(self.range_name), columns = self.worksheet.row_values(3))
            index =self.df[self.df["ID"]=='-'].index
            self.df = self.df.drop(index)
            print('Se conectó a la hoja de datos')
        except Exception as e:
            print('Ocurrió un error. Comuniquece con el administrador.', e)
            
    def ad_in_worksheet(self, url):
        try:
            if url in self.df['url'].tolist():
                return True
            else:
                return False
            
        except Exception as e:
            print('Ocurrió un error. Comuniquece con el administrador.', e)
            
    def actualizar_worksheet(self, append = []):
        try:
            buscados = []
            for url in append:
                buscados.append([url[6]])
            
            if len(append) > 0:
                range_ = self.worksheet.range(name=self.range_name)
                print(self.range_name)
        
                range_first_cell = range_[0]
                range_last_cell = range_[-1]
                data = append
                range_2 = next(x for x in self.ranges_name if x["name"] == self.range_name)
                self.worksheet.delete_named_range(range_2['namedRangeId'])
                self.worksheet.insert_rows(values = data, row=range_last_cell.row + 1)
                self.worksheet.define_named_range(name = '{}:{}'.format(range_first_cell.address, gspread.utils.rowcol_to_a1(range_last_cell.row + len(data), range_last_cell.col)), range_name = self.range_name)
                
            tiempo = time.strftime('%d/%m/%y ; %H:%M:%S')
            self.worksheet.update_acell('B1', tiempo)
            with open('urls_ya_buscadas.csv', 'a') as File:
                writer = csv.writer(File, delimiter =',')
                writer.writerows(buscados)
            print(tiempo)
        except Exception as e:
            print('Ocurrió un error. Comuniquece con el administrador.', e)
         