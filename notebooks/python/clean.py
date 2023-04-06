from abc import ABC, abstractmethod

import pandas as pd
import numpy as np
import os,  sys
import datetime as dt

class Cleaner(ABC):
    @abstractmethod
    def get_processed_data():
        pass

class DrawPointCoordCleaner(Cleaner):
    @staticmethod
    def get_processed_data():
        df = DrawPointCoordCleaner._import_data()
        return df
    
    def _import_data():
        FILE_LOC = '../data/ptfi_1/'
        FILE_NAME = 'DP_block_grade estimates_actual tons_dp coordinate.xlsx'
        
        return pd.read_excel(FILE_LOC + FILE_NAME, sheet_name='DP_Coordinates')

class PCBCCleaner(Cleaner):
    @staticmethod
    def get_processed_data():
        data = PCBCCleaner._import_data()
        preprocessed_data = PCBCCleaner._preprocess_data(data)
        combined_data = PCBCCleaner._combine_data(preprocessed_data)
        
        return combined_data
    
    def _import_data():
        FILE_LOC = '../data/ptfi_1/'
        FILE_NAME = 'DP_block_grade estimates_actual tons_dp coordinate.xlsx'
        
        return {
            'draw_tons': pd.read_excel(FILE_LOC + FILE_NAME, sheet_name='Drawn Tons'),
            'cu_pcbc': pd.read_excel(FILE_LOC + FILE_NAME, sheet_name='Cu_PCBC'),
            'au_pcbc': pd.read_excel(FILE_LOC + FILE_NAME, sheet_name='Au_PCBC'),
        }
        
    def _preprocess_data(data: dict):
        names = {
            'Draw Point Name': 'name'
        }

        cols = list(data['draw_tons'].columns)
        for col_name in cols:
            if isinstance(col_name, dt.datetime):
                names[col_name] = f'{col_name.year}_{col_name.month}'
                
        # Draw Tons
        data['draw_tons'] = data['draw_tons'].rename(
            columns = names
        )

        data['draw_tons'] = data['draw_tons'].set_index('name').astype(float)
        
        # CU PCBC
        data['cu_pcbc'] = data['cu_pcbc'].rename(
            columns = names
        )

        data['cu_pcbc'] = data['cu_pcbc'].set_index('name').astype(float)
        
        # AU PCBC
        data['au_pcbc'] = data['au_pcbc'].rename(
            columns = names
        )

        data['au_pcbc'] = data['au_pcbc'].set_index('name').astype(float)
        
        return data
        
    def _combine_data(pre_d: dict):
        months = list(pre_d['draw_tons'].columns)
        dhids = list(pre_d['draw_tons'].index)
        
        pre_d['draw_tons'].replace(0, np.nan, inplace=True)
        
        headers = [
            'dhid',
            'month',
            'weight',
            'cu',
            'au'
        ]
        
        data = []

        for dhid in dhids:
            for month in months:
                data.append([
                    dhid,
                    month,
                    pre_d['draw_tons'][month][dhid],
                    pre_d['cu_pcbc'][month][dhid],
                    pre_d['au_pcbc'][month][dhid]
                ])
        
        return pd.DataFrame(
            data,
            columns=headers
        ).dropna().reset_index(drop=True)


class DPAssayCleaner(Cleaner):
    @staticmethod
    def get_processed_data():
        pass

