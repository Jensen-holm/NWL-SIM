from bs4 import BeautifulSoup
import requests
import pandas as pd

def find_link(url, text):
    # returns list of matching links
    a_tags = BeautifulSoup(requests.get(url).text, features = 'lxml').find_all('a', href = True)
    return [link['href'] for link in a_tags if link.text == text]

def find_tables_in_comments(url):
    # might take some more time
    return

def find_tbls(url):
    return pd.read_html(url)

def parse_row(self, row):
    return [str(x.string) for x in row.find_all('td')]

# cant remember which order this function returns things in
def sewp_info(self, html):
    spans = html.find_all('span')
    p_tags = html.find_all('p')
    return spans[8].text, spans[9].text, p_tags[1].text.split()[3]

def find_baseball_data(url):

    return
