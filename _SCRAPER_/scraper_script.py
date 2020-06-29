import pandas as pd
import scraper_class
import time as t
import random as rand
import sklearn

def main():


    # load url_data from csv as pandas data frame
    df = pd.read_csv('./URLs.csv', delimiter='#', error_bad_lines=False)



    # iterate over all lines of url data frame and scrape price data of the respected 
    # stores and write them into a csv file called prices

    # # print(df.shape[1])
    # print(df.loc[1][1])
    # # exit()


    ERR_indices = []

    with open('./prices.csv', 'w') as fout:
        csv_sep = ';'

        # header of url data data frame 
        url_data_header = df.columns.values
        # print(url_data_header)
        # exit()

        # write header of prices data csv
        fout.write(csv_sep.join([store_id.strip('url_') for store_id in df.columns.values]) + '\n')
   

        # debug_counter = 0
        for row_index in range(df.shape[0]):
            print('Iteration #: ', str(row_index))

            # prepare/instantize scraper_class objects, arranged as list object
            # each scraper object represents a store to gets scraped
            ScraperObjects = [scraper_class.Scraper([df.loc[row_index][col_index], url_data_header[col_index]]) for col_index in range(1, df.shape[1])]

            # fetch prices by scraping the html responses 
            prices = []
            # to give some time delay in the web sever request to avoid to get recogniced as bot, we do iterate
            # with a rendomized timedelay

            col_index = 1
            for scraper_obj in ScraperObjects:

                try:
                    price = float(scraper_obj.parse_n_select())
                except Exception as e:
                    print(e)
                    price = 'N/A'
                    ERR_indices.append((row_index, col_index))
                    #continue

                    if price == 'scraping_err':
                        print('\n\n' + 80*'!') 
                        print('There are possible changes in the html sheme of store id: ' + url_data_header[col_index] + '\n')
                        print("couldn't scrape any data\n\n" + 80*'!')
                        price = 'N/A'
                    elif price == 'url_err':
                        print('\n\n' + 80*'!') 
                        print('There is no url for store id: ' + url_data_header[col_index] + '\n')
                        print("couldn't scrape any data\n\n" + 80*'!')
                        price = 'N/A'                       
                        #continue

                prices.append(str(price))

                col_index += 1

            print(prices)

            # wait a while to simulate human behavior to avoid web server blockages
            t.sleep(rand.uniform(0, 1))

            # # write the actually price row into the CSV file
            fout.write(df.loc[row_index][0] + csv_sep + csv_sep.join(prices) + '\n')

            if ERR_indices != []:
                with open('./err_log.txt', 'w') as fout_err_report:
                    for index_tuple in ERR_indices:
                        fout_err_report.write('Error occoured by trial to scrape URL: ' + str(df.loc[index_tuple[0]][index_tuple[1]]) + '\n')



            # debug_counter += 1
            # if debug_counter == 1:
            #     break



            

                



if __name__ == '__main__':
    main()