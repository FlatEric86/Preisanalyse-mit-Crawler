import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# to get the fancy ggplot-style 
plt.style.use('ggplot')



# read prices data CSV fila as pandas data frame
# the parameter <engine> is used to avoid encoding problems 
# furthermore we ignore the column 1 which represents store_1
df = pd.read_csv(
    './prices.csv',
    delimiter=',',
    engine='python',
    usecols = [
        'article_name',
        'store_0', 
        'store_2'
    ]
)


# ratio between the price of store_0 (Amazon) and store_2 (Toys For Fun)
price_ratio      = df['store_0'] / df['store_2']
price_ratio.name = 'price ratio [store_0/store_2]'

# absolute price difference of store_0 (Amazon) and store_2 (Toys For Fun)
price_difference = round(abs(df['store_0'] - df['store_2']),2)
price_difference.name = 'absolute price difference [€]'



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
mean_price_ratios = {key:np.nanmean(mean_price_ratios[key]) for key in mean_price_ratios}
mean_price_diff   = {key:np.nanmean(mean_price_diff[key]) for key in mean_price_diff}
        
print(mean_price_ratios['friends'])


######################### DATAPROCESSING RESULT OUTPUT ########################

# do concatenate the new columns price ratio and absolut price difference to
# the dataframe as new dataframe df_out
df_out = pd.concat([df['article_name'], price_ratio.reindex(df.index)], axis=1)
df_out = pd.concat([df_out, price_difference.reindex(df_out.index)], axis=1)



# write the results into a CSV file on drive
df_out.to_csv('./results.csv', sep=',', index=False, encoding='utf-8-sig')


################################ VISUALIZATION ################################

def bar_plot(ax_obj, data_dict, title, y_axes_label, sub_y_label=None):

    width = 0.5
    
    # little sorting action for better look
    labels  = [key for key in data_dict]
    values  = sorted([data_dict[key] for key in data_dict])
    indices = sorted(range(len(values)), key=lambda k: [data_dict[key] for key in data_dict][k])
    labels  = [labels[i].title() for i in indices]

    # do make a bar plot
    ax_obj.bar(np.arange(len(labels)), values, width, color='green', alpha=0.7)

    # cosmetics
    ax_obj.set_title(title)
    if sub_y_label != None:
        ax_obj.set_ylabel(y_axes_label + ' ' + sub_y_label)
    else:
        ax_obj.set_ylabel(y_axes_label)
    ax_obj.set_xticks(indices)
    ax_obj.set_xticklabels(labels)



fig, ax_obj = plt.subplots(1,2, figsize=(12, 4))

i = 0
for title, data_dict in zip(['Mean Price Ratio', 
                             'Absolute Price Difference'
                             ], 
                             [mean_price_ratios, 
                             mean_price_diff
                             ]
                        ):
    if i == 1:                   
        sub_y_label = '[€]'
    else:
        sub_y_label = None
        
    bar_plot(
        ax_obj[i], 
        data_dict, 
        title= title + '\nin terms of Subbrand', 
        y_axes_label=title, 
        sub_y_label=sub_y_label
    )


    i += 1

plt.savefig('./result_visualization.png')
#plt.show()



















