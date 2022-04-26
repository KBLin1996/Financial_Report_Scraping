# Self-defined files
import config
import margin_statements

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


option = webdriver.ChromeOptions()
option.add_argument('headless')


def fetch_website(stock_symbol, report_type):
    path = f'https://finance.yahoo.com/quote/{stock_symbol}/{report_type}?p={stock_symbol}'

    driver = webdriver.Chrome(options=option)
    driver.get(path)

    # Since Yahoo Finance operates on JavaScript, running the code through this method pulls all of
    # the data and saves it as if it were a static website
    html = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(html, 'lxml')

    return soup


def fetch_statements(soup, indicators):
    header_list = list()
    row_list = list()
    label_list = list()
    final_list = list()

    features = soup.find_all('div', class_='D(tbr)')

    # Create headers
    for item in features[0].find_all('div', class_='D(ib)'):
        header_list.append(item.text)
    
    # Statement contents
    for index in range(len(features)):
        # Fetch each element from the report
        statement = features[index].find_all('div', class_='D(tbc)')

        is_indicator = False
        for content in statement:
            content = content.text.strip()

            # Check if the current statement is in our indicators
            if content in indicators or is_indicator:
                is_indicator = True

                # Add each item to row list
                row_list.append(content)

            # If not, we skip this statement
            else:
                break
        
        # Add the statement into the final list
        if len(row_list) > 0:
            final_list.append(row_list)
        
            # Clear row_list
            row_list = list()

    df = pd.DataFrame(final_list)
    df.columns = header_list

    return df


def clean_dataframe(df: pd.DataFrame, convert_title_dict: dict) -> pd.DataFrame():
    df = df.fillna('-')

    # Replace some statements' titles based on the convert_title_dictionary from config.py
    df['Breakdown'] = df['Breakdown'].replace(convert_title_dict)

    return df


def organize_reports(stock_symbol: str, report_types: list, indicators: list) -> pd.DataFrame():
    df = pd.DataFrame()

    for report in report_types:
        soup = fetch_website(stock_symbol, report)

        # Concatenate all reports
        df = pd.concat([df, fetch_statements(soup, indicators)], ignore_index=True)

    return df


if __name__ == '__main__':
    with pd.ExcelWriter(config.save_path) as writer:
        for stock_symbol in config.stock_symbols:
            # Fetch all given stock symbol's reports in HTML format from Yahoo finanace and extract the
            # indicators we want from them
            df = organize_reports(stock_symbol, config.report_types, config.indicators)

            # Filter all nan values and replace some statements' titles
            df = clean_dataframe(df, config.convert_title_dict)

            # Add margin statements into the dataframe
            df = margin_statements.add_margin_statements(df)

            # Drop titles that are only for margin calculation
            df = margin_statements.drop_margin_statements(df, config.drop_titles)

            # Store the dateframe in a specific sheet and named it according to its stock symbol
            df.to_excel(writer, sheet_name=stock_symbol, index=False)

            print(f"Done scraping {stock_symbol}")

    print(f"\nSuccessfully saved financial all report!\n-> Path: {config.save_path}\n")