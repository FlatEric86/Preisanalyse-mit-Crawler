import pandas as pd
import numpy as np

# read prices data CSV fila as pandas data frame
# the parameter <engine> is used to avoid encoding problems 
# furthermore we ignore the column of store_1
df = pd.read_csv('./prices.csv',
    delimiter=';',
    engine='python',
    usecols = ['article_name','store_0', 'store_2'])


# ratio between the price of store_0 (Amazon) and store_2 (Toys For Fun)
price_ratio      = df['store_0'] / df['store_2']

# absolut price difference of store_0 (Amazon) minus store_2 (Toys For Fun)
price_difference = abs(df['store_0'] - df['store_2'])

print(price_difference)