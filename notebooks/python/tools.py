import pandas as pd


def clean_data(data: pd.DataFrame):
    """
    Takes in a pandas DataFrame object and cleans it of NaN values. 
    Then sorts and reindexes the DataFrame before passing the data back to the caller.

    Args:
        data (pd.DataFrame): A pandas DataFrame to be cleaned, sorted, and reindexed

    Returns:
        _type_: _description_
    """
    data = data.dropna(axis=0)
    data = data.sort_values(by='grade', ascending=False)
    data = data.reset_index(drop=True)
    
    return data

def get_year_month(i):
    FIRST_YEAR, FIRST_MONTH = 2015, 7 # 7 is August
    year = FIRST_YEAR + int((FIRST_MONTH + i) / 12)
    month = (FIRST_MONTH + i) % 12
    return year, month

def get_points(elapsed_months, df) -> str:
    year, month = get_year_month(elapsed_months)
    return df[f'{year}_{month + 1}']