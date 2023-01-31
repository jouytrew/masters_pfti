import numpy as np
import pandas as pd

class Resource:
    def __init__(self, weights: np.array, grades: np.array):
        data = {
            'weight': weights,
            'grade': grades
        }
        
        cleaned_info = self.clean_data(pd.DataFrame(data))
        
        # after cleaning, check if there is data
        
        self.info = self.calculate_derived_data(cleaned_info)
        self.calculate_intermediate(self.info)
        self.heterogeneity = self.calculate_heterogeneity(self.info)
             
    def clean_data(self, data: pd.DataFrame):
        # data = data.replace(-9, np.nan)
        data = data.dropna(axis=0)
        data = data.sort_values(by='grade', ascending=False)
        data = data.reset_index(drop=True)
        
        return data
    
    def calculate_derived_data(self, cleaned_info: pd.DataFrame):
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
    
    def calculate_intermediate(self, df):
        if len(df) > 0:
            b = df['weight']
            c = df['cml_grade'].iloc[-1]
            d = sum(df['weight'])
            a = np.subtract(df['grade'], c)

            num, den = np.multiply(a, b), np.multiply(c, d)
            df['int_het'] = np.power(np.divide(num, den), 2)  # (num/den)^2
        
    def calculate_heterogeneity(self, df):
        if len(df) > 0:
            return len(df) * sum(df['int_het'])
        else:
            return np.NaN

    
class Grouping:
    def __init__(self, id):
        self.id = id
        self.resources = {}
        
    def add_resource(self, resource_id: str, weights: np.array, grades: np.array):
        if len(weights) == len(grades):
            if len(weights) > 0:
                self.resources[resource_id] = Resource(weights, grades)
            else:
                self.resources[resource_id] = None
                print(f"No data for grouping: {self.id}, {resource_id}")
        else:
            raise Exception(f"[Grouping ID: {id}] Weight and grade arrays must be same length.")