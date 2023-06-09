import numpy as np
import pandas as pd
import tools

# This file is being depreceated

class Resource:
    def __init__(self, cleaned_info: pd.DataFrame):
        self._info = self.__calculate_derived_data(cleaned_info)
        self.__calculate_intermediate(self._info)
        self._heterogeneity = self.__calculate_heterogeneity(self._info)
    
    # def clean_data(self, data: pd.DataFrame):
    #     # data = data.replace(-9, np.nan)
    #     data = data.dropna(axis=0)
    #     data = data.sort_values(by='grade', ascending=False)
    #     data = data.reset_index(drop=True)
    
    #     return data
    
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

    
class Grouping:
    def __init__(self, id):
        self.id = id
        self.resources = {}
        
    def add_resource(self, resource_id: str, weights: np.array, grades: np.array):
        # Check if the arrays are the same length
        if len(weights) == len(grades):
            # Clean data
            cleaned_data = tools.clean_data(
                pd.DataFrame({
                    'weight': weights,
                    'grade': grades
                })
            )
            
            # Check if there is data after cleaning
            if len(cleaned_data) > 0:
                self.resources[resource_id] = Resource(cleaned_data)
            else:
                # TODO: raise error to be handled
                print(f"No data for grouping: {self.id}, resource: {resource_id}")
        else:
            raise Exception(f"[Grouping ID: {id}] Weight and grade arrays must be same length.")