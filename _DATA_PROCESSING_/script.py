import pandas as pd
import numpy as np

# read prices data CSV fila as pandas data frame
# the parameter <engine> is used to avoid encoding problemes 
df = pd.read_csv('./prices.csv', delimiter=';',engine='python')


print(df.head())