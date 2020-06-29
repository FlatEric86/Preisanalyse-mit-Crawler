from bs4 import BeautifulSoup
import requests
import random as rand
import time as t

class Scraper:

    def __init__(self, url_and_store_name):

        self.url      = url_and_store_name[0]
        self.store_id = url_and_store_name[1]

        self.headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})  
  
    # def set_url(self, url_and_store_id):
        
    #     self.url      = url_and_store_id[0]
    #     self.store_id = url_and_store_id[1]

    def __conv_prc_strng_to_flt(self, prod_price):
        # slice off unicode space and '€'
        prod_price = prod_price.replace('\xa0€','')
        
        # replace 'comma' by '.'
        prod_price = prod_price.replace(',', '.')
        
        return float(prod_price)



    def parse_n_select(self):

        if self.url == 'N/A':
            return 'url_err'
    
        # get html response from web server by url
        # we are using 3 times of trial to get response from web server
        # and add some randomized time delay after each failed trial
        # trial = 0
        # while trial < 3:
        #     try:   
        #         response = requests.get(self.url, headers=self.headers)
        #         break
        #     except Exception as e:
        #         pass
        #     trial += 1

        #     t.sleep(rand.uniform(0,3))

        # if trial == 3:
        #     return e

        response = requests.get(self.url, headers=self.headers)

        # parse html response
        try:
            parsed = BeautifulSoup(response.content, features='lxml')
        except Exception as e:
            print(e)
            return e
        

        # fetch the significant features from parsed html depended on
        # kind of store (every store uses its own html sheme...)
        # currently, its just the price of the article
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        if self.store_id == 'url_store_0':
            #print('amazon')
            
        
            # product price (html tag is: #priceblock_ourprice)
            try:
                prod_price = parsed.select('#priceblock_ourprice')[0].get_text().strip()
                prod_price = self.__conv_prc_strng_to_flt(prod_price)
            except Exception as e:
                print(e)
                return e
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        if self.store_id == 'url_store_1':
            #print('spielemax')

            try:
                ScriptContents = parsed.findAll('script')
                
                break_loop = False
                for script in ScriptContents:
                    script_c = ''.join(script.findAll(text=True)).split('\n')

                    for line in script_c:
                        if 'ecomm_totalvalue' in line:
                            break_loop = True
                            break

                    if break_loop == True:
                        break


                ## extract price value of line
                signf_elem = line.split(',')[-1]
                # replace some chars
                signf_elem = ''.join(c for c in signf_elem if c not in ['{', '}', '[', ']', '=', ';'])

                try:
                    prod_price = float(signf_elem.split(':')[-1])
                except Exception as e:
                    print(e)
                    return e

                # for case that the scraping trial fails (by changed html sheme etc.)
                # handle back this error to main script
                if break_loop == 0:
                    return 'scraping_err'

                
            except Exception as e:
                print(e)
                return e        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        if self.store_id == 'url_store_2':
            #print('Toys for fun')

            try:
                price_raw = parsed.find('span', {'class': 'price'}).text
            except Exception as e:
                print(e)
                return e

            prod_price = self.__conv_prc_strng_to_flt(price_raw)

        return prod_price
        
    


    
#### debugging/testing

# url = 'https//www.python.org'


### AMAZON 
# url = 'https://www.amazon.de/Lego-41369-Friends-Mias-Pferd/dp/B07FP2KS3N'
#url = 'https://www.amazon.de/LEGO-76124-Kinderspielzeug-Bunt/dp/B07FP2GRY3'
#url = 'https://www.amazon.de/41428-Friends-Beach-House-Multi-Colour/dp/B0813RJRYG'
# url = 'https://www.amazon.de/LEGO-42098-Technic-Autotransporter/dp/B07NDBSR45'
       
# scraper_obj = Scraper([url, 'url_store_0'])
# print(scraper_obj.parse_n_select())


### SPIELEMAX

#url = 'https://www.spielemax.de/lego-technic-42099-allrad-xtreme-gelandewagen-240688.html'
#url = 'https://www.spielemax.de/lego-friends-41380-leuchtturm-mit-flutlicht-236696.html'
#url = 'https://www.spielemax.de/lego-friends-41430-wasserpark-von-heartlake-city-258879.html'
# url  = 'https://www.spielemax.de/lego-friends-41428-strandhaus-mit-tretboot-258864.html'



       
# scraper_obj = Scraper([url, 'url_store_1'])
# print(scraper_obj.parse_n_select())



### TOSY FOR FUN


#url = 'https://www.toys-for-fun.com/de/42092-rettungshubschrauber.html'
#url = 'https://www.toys-for-fun.com/de/41369-mias-haus-mit-pferd.html'
#url = 'https://www.toys-for-fun.com/de/legor-friends-41428-strandhaus-mit-tretboot.html'
# url = 'https://www.toys-for-fun.com/de/41378-rettungs-u-boot-fuer-delfine.html'


# scraper_obj = Scraper([url, 'url_store_2'])
# print(scraper_obj.parse_n_select())





























# headers = ({'User-Agent':
            # 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            # 'Accept-Language': 'en-US, en;q=0.5'})

# url        = 'https://www.amazon.de/Lego-41369-Friends-Mias-Pferd/dp/B07FP2KS3N'


# response   = requests.get(url, headers=headers)

# soup       = BeautifulSoup(response.content, features='lxml')

# prod_title = soup.select('#productTitle')[0].get_text().strip()
# prod_price = soup.select('#priceblock_ourprice')[0].get_text().strip().split(' ')[0]

# print(prod_title)
# print(prod_price)


