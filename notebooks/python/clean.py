from abc import ABC, abstractmethod

import pandas as pd
import numpy as np
import datetime as dt

class Cleaner(ABC):
    @abstractmethod
    def get_processed_data():
        pass

class DrawPointCoordCleaner(Cleaner):
    @staticmethod
    def get_processed_data():
        imported_data = DrawPointCoordCleaner._import_data()
        processed_data = DrawPointCoordCleaner._process_data(imported_data)
        return processed_data
    
    def _process_data(data: pd.DataFrame):
        data = data.rename(
            columns={
                "Draw Point Name": "name", 
                "X-dpt": "x",
                'Y-dpt': 'y',
                'Z-dpt': 'z'
            }
        )
        data = data.set_index('name')
        return data
    
    def _import_data():
        FILE_LOC = '../data/ptfi_1/'
        FILE_NAME = 'DP_block_grade estimates_actual tons_dp coordinate.xlsx'
        
        return pd.read_excel(FILE_LOC + FILE_NAME, sheet_name='DP_Coordinates')

class PCBCCleaner(Cleaner):
    # @staticmethod
    # def get_processed_and_filtered_data():
    #     pcbc_df = PCBCCleaner.get_processed_data()
        
    #     earliest_dp = dt.date(2020, 10, 2)  # Earliest date in the drawpoints dataset
    #     filtered_df = pcbc_df.query('date > @earliest_dp')
        
    #     return pcbc_df, filtered_df
    
    @staticmethod
    def _filter_data(data):
        earliest_dp = dt.date(2020, 10, 2)  # Earliest date in the drawpoints dataset
        filtered_data = data.query('date > @earliest_dp')
        
        return filtered_data     
    
    @staticmethod
    def get_processed_data():
        imported_data = PCBCCleaner._import_data()
        preprocessed_data = PCBCCleaner._preprocess_data(imported_data)
        combined_data = PCBCCleaner._combine_data(preprocessed_data)
        
        # return combined_data
        
        filtered_data = PCBCCleaner._filter_data(combined_data)
        return filtered_data
    
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

        # cols = list(data['draw_tons'].columns)
        # for col_name in cols:
        #     if isinstance(col_name, dt.datetime):
        #         names[col_name] = f'{col_name.year}_{col_name.month}'
                
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
            'date',
            'weight',
            'CU',
            'AU'
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

class DrawPointAssayCleaner(Cleaner):
    @staticmethod
    def get_processed_data():
        data = DrawPointAssayCleaner._import_data()
        preprocessed_data = DrawPointAssayCleaner._preprocess_data(data)
        combined_data = DrawPointAssayCleaner._combine_duplicates(preprocessed_data)
        
        return combined_data
        
    def _import_data():
        return pd.read_csv("../data/ptfi_1/dmlz_assay.csv")
    
    def _preprocess_data(data: pd.DataFrame):
        data['Tons_Sampling'] = data['Tons_Sampling'].astype(float)

        # Rename all the columns to a capitalized element code i.e. "CU", "AU"
        rename_cols = list(data.columns)[7:-1]
        for col in rename_cols:
            data = data.rename(columns={col: col.split('_')[0].upper()})
        
        names = {
            'HOLEID': 'dhid',
            'DATESAMPLED': 'date',
            'SampleWeight': 'weight'
        }
        
        data = data.rename(columns=names)    
        
        data['date'] = pd.to_datetime(data['date'])
        
        return data
    
    # Take the repeated `SAMPLEID` values and combine them as they shouldn't be treated as independent values
    def _combine_duplicates(data: pd.DataFrame):
        # idxs = [
        #     [16209, 16210],
        #     [18704, 18705],
        #     [18739, 18740]
        # ]
        # data.iloc[np.array(idxs).flatten()]

        # SAMPLE_WEIGHT = 'SampleWeight'
        # numeric_cols = list(assay.columns)[7:-1]

        # idxs = [
        #     [16209, 16210],
        #     [18704, 18705],
        #     [18739, 18740]
        # ]
        # assay.iloc[np.array(idxs).flatten()]

        # TODO: combine the data from the same samples

        # for combine_ids in idxs:
        #     w = []
        #     sample_data = {}
            
        #     for id in combine_ids:
        #         row = assay.loc[id]
                
        #         w.append(row[SAMPLE_WEIGHT])
        #         for col in numeric_cols:
        #             if col not in sample_data:
        #                 sample_data[col] = [row[col]]
        #             else:
        #                 sample_data[col].append(row[col])
            
        #     combined_sample = {}
                    
        #     sample = assay.loc[combine_ids[0]].to_dict()
            
        #     for id in combine_ids[1:]:
        #         sample_add = assay.loc[id]
                
        #         for col in numeric_cols:
        #             if np.isnan(sample_add[col]):
        #                 sample[col] = np.nan
        #             else:
        #                 sample[col] = (sample[col] * sample[SAMPLE_WEIGHT]) + (sample_add[col] * sample_add[SAMPLE_WEIGHT]) / (sample[SAMPLE_WEIGHT] + sample_add[SAMPLE_WEIGHT])
        #         sample[SAMPLE_WEIGHT] += sample_add[SAMPLE_WEIGHT]
            
        #     assay = assay.drop(axis=0, index=combine_ids)
        #     df_dictionary = pd.DataFrame([sample])
        #     assay = pd.concat([assay, df_dictionary], ignore_index=True)

        return data

class BlockModelCleaner(Cleaner):
    @staticmethod
    def get_processed_data():
        imported_data = BlockModelCleaner._import_data()
        preprocessed_data = BlockModelCleaner._preprocess_data(imported_data)
        
        return preprocessed_data
    
    def _import_data():
        BM_ROOT = '../data/ptfi_2/dh_and_bm_data/DMLZ_Block_Model/'
        return pd.read_csv(BM_ROOT + 'block_model.csv', index_col=0)
        
    def _preprocess_data(data: pd.DataFrame):
        names = {
            'ag': 'AG',
            'au': 'AU',
            'cu': 'CU'
        }

        data = data.rename(
            columns = names
        )
        
        return data


class DrillholeAssayCleaner(Cleaner):
    pass

def group_by_dhid():
    # write some code to group by dhids
    pass

