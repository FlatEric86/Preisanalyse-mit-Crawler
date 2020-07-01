import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter


# to get the fancy ggplot-style in pyplot plots
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

mean_prices_store_0 = pd.Series([df['store_0'][df['article_name'].str.contains(key, case=False)].mean() for key in sub_brands])
mean_prices_store_2 = pd.Series([df['store_2'][df['article_name'].str.contains(key, case=False)].mean() for key in sub_brands])


def bar_plot_0(ax_obj):

    width = 0.5
    
    # do compute the ratio of mean prices over all subbrands
    difference = mean_prices_store_0 - mean_prices_store_2
    
    # do sorting the series for better look in visualization
    difference = difference.sort_values()
    labels     = [sub_brands[i].title() for i in difference.index]

    # make bar plot
    ax_obj.bar(np.arange(len(sub_brands)), difference, width, color='green', alpha=0.8)

    # some cosmetics like axes labels, title etc.
    ax_obj.set_title('Mean Price Difference\nin Terms of Subbrand\n$_{Amazon\ -\ Toys\ for\ Fun}$')
    ax_obj.set_ylabel('Mean Price Diffrence [€]')
    ax_obj.set_xticks(list(range(len(sub_brands))))
    ax_obj.set_xticklabels(labels)


def bar_plot_1(ax_obj):

    width = 0.5
    
    # do compute the ratio of mean prices over all subbrands
    ratio = mean_prices_store_0 / mean_prices_store_2
    
    # do sorting the series for better look in visualization
    ratio = ratio.sort_values()
    labels     = [sub_brands[i].title() for i in ratio.index]

    # make bar plot
    ax_obj.bar(np.arange(len(sub_brands)), ratio, width, color='cornflowerblue', alpha=0.8)

    # some cosmetics like axes labels, title etc.
    ax_obj.set_title('Mean Price Ratio\nin Terms of Subbrand\n$_{Amazon\ /\ Toys\ for\ Fun}$')
    ax_obj.set_ylabel('Mean Price Ratio [€/€]')
    ax_obj.set_xticks(list(range(len(sub_brands))))
    ax_obj.set_xticklabels(labels)



def bar_plot_2(ax_obj):
     
    width = 0.25
    
    # mean price of both stores per subbrand
    pd_series = 0.5*(mean_prices_store_0 + mean_prices_store_2)
    
    # to reorder the Series in ascanding wise by using the mean value of each price tuple of subbrand
    resorted_indices = pd_series.sort_values().index
    
   
    ax_obj.bar(np.arange(len(sub_brands)) - width/2, mean_prices_store_0.reindex(resorted_indices), width, label='Amazon', alpha=0.8)
    ax_obj.bar(np.arange(len(sub_brands)) + width/2, mean_prices_store_2.reindex(resorted_indices), width,label='Toys for Fun', alpha=0.8) 
    labels = [sub_brands[i].title() for i in list(resorted_indices)]

    # cosmetics
    ax_obj.set_title('Prices in Terms of Subbrand and Store')
    ax_obj.set_ylabel('Mean Price [€]')
    ax_obj.set_xticks(list(range(len(sub_brands))))
    ax_obj.set_xticklabels([label.title() for label in labels])
    ax_obj.legend()



def box_plot(ax_obj):
     
    width = 0.25
    

    # both price data column filtered by nan to avoid runtime problems at using boxplot function
    all_data = [
        df['store_0'][~np.isnan(df['store_0'])],
        df['store_2'][~np.isnan(df['store_2'])],

    ]




    # scatter plot of the 


    # cosmetics
    ax_obj.set_title('Price Ranges of the two Stores')
    ax_obj.set_ylabel('Price [€]')
    ax_obj.boxplot(all_data, notch=True, sym="o", labels=['Amazon', 'Toys for Fun'])
    #ax_obj.legend()






fig = plt.subplots(squeeze=False, figsize=(14, 8))
ax0 = plt.subplot2grid((2, 2), (0, 0))
ax1 = plt.subplot2grid((2, 2), (0, 1))
ax2 = plt.subplot2grid((2, 2), (1, 0))
ax3 = plt.subplot2grid((2, 2), (1, 1))

bar_plot_0(ax0)
bar_plot_1(ax1)
bar_plot_2(ax2)
box_plot(ax3)

plt.savefig('./result_visualization.png')

plt.show()



















