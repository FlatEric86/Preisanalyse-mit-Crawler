import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter


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
        



######################### DATAPROCESSING RESULT OUTPUT ########################

# do concatenate the new columns price ratio and absolut price difference to
# the dataframe as new dataframe df_out
df_out = pd.concat([df['article_name'], price_ratio.reindex(df.index)], axis=1)
df_out = pd.concat([df_out, price_difference.reindex(df_out.index)], axis=1)



# write the results into a CSV file on drive
df_out.to_csv('./results.csv', sep=',', index=False, encoding='utf-8-sig')






################################ VISUALIZATION ################################

def bar_plot_1(ax_obj, data_dict, title, y_axes_label, sub_y_label=None):

    width = 0.5
    
    # little sorting action for better look
    sort_tuples = sorted([[key_, data_dict[key_]] for key_ in data_dict], key=itemgetter(1))
    labels  = [item[0].title() for item in sort_tuples]
    values  = [item[1] for item in sort_tuples]

    
    # do make a bar plot
    ax_obj.bar(np.arange(len(labels)), values, width, color='green', alpha=0.7)

    # cosmetics
    ax_obj.set_title(title)
    if sub_y_label != None:
        ax_obj.set_ylabel(y_axes_label + ' ' + sub_y_label)
    else:
        ax_obj.set_ylabel(y_axes_label)
    ax_obj.set_xticks(list(range(len(labels))))
    ax_obj.set_xticklabels(labels)




def bar_plot_0(ax_obj):
    
    
    mean_prices_store_0 = [df['store_0'][df['article_name'].str.contains(key, case=False)].mean() for key in sub_brands]
    mean_prices_store_2 = [df['store_2'][df['article_name'].str.contains(key, case=False)].mean() for key in sub_brands]
    
    width = 0.25
    
    rects1 = ax_obj.bar(np.arange(len(sub_brands)) - width/2, mean_prices_store_0, width, label='Amazon')
    rects2 = ax_obj.bar(np.arange(len(sub_brands)) + width/2, mean_prices_store_2, width,label='Toys for Fun') 
    # ax_obj.bar(np.arange(len(sub_brands)), mean_prices_store_0, width, color='green', alpha=0.7)


    # cosmetics
    ax_obj.set_title('Mean Prices in Terms of Subbrand')
    ax_obj.set_ylabel('Mean Price [€]')
    ax_obj.set_xticks(list(range(len(sub_brands))))
    ax_obj.set_xticklabels(sub_brands)
    ax_obj.legend()






fig, ax_obj = plt.subplots(2,2, figsize=(14, 6))

i = 0
for title, data_dict in zip(['Mean Price Ratio', 
                             'Absolute Mean Price Difference'
                             ], 
                             [mean_price_ratios, 
                             mean_price_diff                            
                             ],

                        ):
    if i == 1:                   
        sub_y_label = '[€]'
        sub_title   = ''
    else:
        sub_y_label = None
        sub_title   = sub_title   = '$_{Amazon\ /\ Toys\ for\ Fun}$'
        
    bar_plot_1(
        ax_obj[0][i], 
        data_dict, 
        title=title + '\nin Terms of Subbrand\n' + sub_title, 
        y_axes_label=title, 
        sub_y_label=sub_y_label
    )


    i += 1


bar_plot_0(ax_obj[1][0])

plt.savefig('./result_visualization.png')

plt.show()



















