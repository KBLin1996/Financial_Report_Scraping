import config
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def fetch_website(stock_symbol, report_type):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    path = f'https://finance.yahoo.com/quote/{stock_symbol}/{report_type}?p={stock_symbol}'

    # Reference: https://selenium-python.readthedocs.io/api.html
    driver = webdriver.Chrome(executable_path='./chromedriver', options=option)
    driver.get(path)

    # Since Yahoo Finance operates on JavaScript, running the code through this method pulls all of
    # the data and saves it as if it were a static website
    html = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(html, 'lxml')

    return soup


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame():
    df = df.fillna('-')

    # Replace some statements' titles based on the convert_title_dictionary from config.py
    df['Breakdown'] = df['Breakdown'].replace(config.convert_title_dict)

    return df
