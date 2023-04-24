import numpy as np
import pandas as pd

class HetAnalysis:
    def __init__(self, id: str, weights: np.array, grades: np.array):
        if len(weights) == len(grades) and len(weights) > 0:
            info = pd.DataFrame({
                'weight': weights,
                'grade': grades
            })
            cleaned_info = self.clean_data(info)
            self._info = self.__calculate_derived_data(cleaned_info)
            self.__calculate_intermediate(self._info)
            self._heterogeneity = self.__calculate_heterogeneity(self._info)
        else:
            raise Exception('Hi')
             
    def clean_data(self, data: pd.DataFrame):
        # data = data.replace(-9, np.nan)
        data = data.dropna(axis=0)
        data = data.sort_values(by='grade', ascending=False)
        data = data.reset_index(drop=True)
        
        return data
    
    def __calculate_derived_data(self, cleaned_info: pd.DataFrame):
        df = cleaned_info
        df['cml_weight'] = df['weight'].cumsum()
    
        sum_weights = sum(df['weight'])
        df['weight_pct'] = np.divide(df['weight'], sum_weights)
        df['cml_weight_pct'] = df['weight_pct'].cumsum()
        df['yield'] = np.multiply(df['weight'], df['grade'])
        df['cml_yield'] = df['yield'].cumsum()
        df['cml_grade'] = np.divide(df['cml_yield'], df['cml_weight'])
        
        sum_yield = sum(df['yield'])
        df['recovery'] = np.divide(df['yield'], sum_yield)
        df['cml_recovery'] = df['recovery'].cumsum()
        
        return df
    
    def __calculate_intermediate(self, df):
        if len(df) > 0:
            b = df['weight']
            c = df['cml_grade'].iloc[-1]
            d = sum(df['weight'])
            a = np.subtract(df['grade'], c)

            num, den = np.multiply(a, b), np.multiply(c, d)
            df['int_het'] = np.power(np.divide(num, den), 2)  # (num/den)^2
    
    def __calculate_heterogeneity(self, df):
        if len(df) > 0:
            return len(df) * sum(df['int_het'])
        else:
            return np.NaN
        
    def get_heterogeneity(self):
        return self._heterogeneity
    
    def get_info(self):
        return self._info
    
    def get_grade(self):
        return self._info['cml_grade'].iloc[-1]
    
    def get_cml_weight(self):
        return self._info['cml_weight'].iloc[-1]
