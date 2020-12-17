import requests as rq
from bs4 import BeautifulSoup

class Alibaba():

    def __init__(self, url):

        self.url = url
        self.response = rq.get(url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def find_product_name(self):
        name = self.soup.find('h1', class_='ma-title').get('title')
        return {"name" : name}

    def find_product_price_data(self):

        price_wrap = self.soup.find('div', class_='ma-price-wrap')

        price_is_multiple = False

        price_info = {}

        try:
            price_info['price'] = self.soup.find('span', class_='ma-ref-price').text.split("\n")[1]
            price_info['min_order'] = self.soup.find('span', class_='ma-min-order').text
        except:
            price_is_multiple = True



        quantity_range = ""
        promotion_price = ""
        original_price = ""

        if (price_is_multiple):

            for li in price_wrap.find_all('li'):

                there_is_promotion_price = False

                try:
                    promotion_price = li.find('div', class_= 'ma-spec-price ma-price-promotion').find('span').get('title')
                    there_is_promotion_price = True
                except:
                    there_is_promotion_price = False


                if(there_is_promotion_price):
                    quantity_range = li.find('div', class_="ma-quantity-range").get('title')
                    try:
                        original_price = li.find('div', class_='ma-spec-price ma-price-original').find('span').get('title')
                        price_info[quantity_range] = {'promotion_price' : promotion_price, 'original_price' : original_price}
                    except:
                        price_info[quantity_range] = {'price' : promotion_price,}

                else:
                    original_price = li.find('div', class_='ma-spec-price').find('span').text

                    quantity_range = li.find('span', class_="ma-quantity-range").get('title')
                    price_info[quantity_range] = {'price' : original_price}

        return price_info

    def find_supplier_name_url(self):

        company_name_container = self.soup.find('div', class_='company-name-container')

        company_name = company_name_container.find('a').get('title')
        company_url = company_name_container.find('a').get('href')

        return {'company_name' : company_name, 'company_url' : company_url}

    def find_supplier_country(self):

        card_supplier = self.soup.find('div', class_='card-supplier card-icons-lite')

        country = ""
        yearsofoperation = ""

        try:
            country = card_supplier.find('span', class_='register-country').text
        except:
            country = "Unknown"

        return {
            'country' : country,
        }

    def find_supplier_category(self):

        category = ''

        try:
            card_central_logo = self.soup.find('div', class_='card-central-logo')
            category = card_central_logo.find('a').get('title')
        except:
            category = "Unknown"




        return {'category' : category}

    def find_supplier_response_rate(self):

        response_rate = ""

        try:
            widget_supplier_card = self.soup.find('div', class_='widget-supplier-card')

            ratings_table = widget_supplier_card.find('table')

            response_rate = ratings_table.find('a', class_='performance-value-wrap').find('b').text
        except:

            response_rate = "Unknown"

        return response_rate
