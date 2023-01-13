import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

class webscrapping():

    def scrape_html(self, base_url, page):
        """
        Sending a GET request to and creating a BeautifulSoup object

        """
        self.base_url = base_url
        self.page = page
        url = base_url + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        return soup

    def get_page_content(self, soup):
        self.soup = soup
        products_info_content = soup.find_all('div', class_='product-card__content')
        return products_info_content

    def get_page_price(self, soup):
        self.soup = soup
        products_info_price = soup.find_all('div', class_='product-card__data')
        return products_info_price

    def get_product_name(self, products_info_content):
        self.products_info_content = products_info_content
        product_name = []
        for product in range(len(products_info_content)):
            name_p = products_info_content[product].find_all('p')[0]
            alcohol_name = name_p.contents[0].strip()

            product_name.append(alcohol_name)
        return product_name

    def creat_df(self, name):
        self.name = name
        original_df = pd.DataFrame(name, columns=['Product_Name'])
        return original_df

    def insert_into_df(self, original_df, new_df):
        self.original_df = original_df
        self.new_df = new_df

        original_df = original_df.append(new_df, ignore_index=True, verify_integrity=True)
        return original_df

    def get_links(self, url=''):
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        a_tags = soup.find_all('a', class_='subnav__link')
        links_list = []
        for link in a_tags:
            links_list.append(link.get('href'))

        relevant_links = []
        for link in links_list:
            if link is not None and '/c/' in link and 'whiskey' in link and '?' not in link:
                relevant_links.append(link)

        return relevant_links

    def scrape_whiskey(self, url='https://www.thewhiskyexchange.com', number_of_pages=5):
        self.url = url
        self.number_of_pages = number_of_pages
        df = pd.DataFrame()
        s = webscrapping()
        links = s.get_links(url=url)

        for link in links:
            try:
                for page in range(0, number_of_pages):
                    soup = s.scrape_html(base_url=url+page+'?pg=', page=page+1)
                    content_html = s.get_page_content(soup)
                    price_html = s.get_page_price(soup)
                    names = s.get_product_name(content_html)
                    if page == 0:
                        data = s.creat_df(name=names)

                    data = s.insert_into_df(data, s.creat_df(name=names))
                # ...
            except:
                print("Error with the link: {}".format(link))
            finally:
                start_location = link.rfind('/') + 1
                end_location = len(link)
                data.to_csv(link[start_location:end_location] + '.csv')
                df = df.append(data, ignore_index=True)
            
        return df

print(webscrapping().scrape_whiskey())