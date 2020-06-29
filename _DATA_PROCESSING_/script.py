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
price_ratio.name = 'price ratio [store_0/store_2]'

# absolute price difference of store_0 (Amazon) and store_2 (Toys For Fun)
price_difference = abs(df['store_0'] - df['store_2'])
price_difference.name = 'absolute price difference'



# list about all sub brands of the lego items
sub_brands = [
    'technic',
    'friends',
    'marvel',
    'harry potter',
    'duplo'
]

# hash list to store mean values of price ratios associated to their subbrand
mean_price_ratios = {key:[] for key in sub_brands}

# hash list to store mean values of price differeces associated to their subbrand
mean_price_diff = {key:[] for key in sub_brands}

# do iterate over all rows of data frame and select by subbrand id and store the
# associated price ratio into the mean_price_ratios dictionary.
for index, row in df.iterrows():
    for sub_br in sub_brands:
        if sub_br in row[0].lower(): 
            mean_price_ratios[sub_br].append(price_ratio[index])
            mean_price_diff[sub_br].append(price_difference[index])
 
 
# do compute the mean values of the price ratios by using meannan at each list
# associatet with the respected key
# we use nanmean because some NAN may occur during data problems
mean_price_ratios = {key:np.nanmean(mean_price_ratios[key]) for key in mean_price_ratios}
mean_price_diff   = {key:np.nanmean(mean_price_diff[key]) for key in mean_price_diff}
        


######################### DATAPROCESSING RESULT OUTPUT ########################

# do concatenate the new columns price ratio and absolut price difference to
# the dataframe as new dataframe df_out
df_out = pd.concat([df, price_ratio.reindex(df.index)], axis=1)
df_out = pd.concat([df_out, price_difference.reindex(df_out.index)], axis=1)








################################ VISUALIZATION ################################
























