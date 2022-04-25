import config
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


def calculate_margin(numerator_list: list, denominator_list: list, is_percentage: bool):
    result = list()

    for i in range(len(numerator_list)):
        if numerator_list[i] == "-" or denominator_list[i] in ["-", "0"]:
           result.append("-")
           continue

        numerator = eval(numerator_list[i].replace(",", ""))
        denominator = eval(denominator_list[i].replace(",", ""))

        if is_percentage:
            result.append("{:.2f} %".format(numerator * 100 / denominator))
        else:
            result.append("{:.2f}".format(numerator / denominator))

    return result


# Since Yahoo finance did not support margin data in reports, we have to calculate them manually
def add_margin_statements(df: pd.DataFrame()) -> pd.DataFrame():
    # Set up all statements we want to add on the dataframe
    interest_coverage = ['Interest Coverage']
    net_margin = ['Net Margin']
    gross_margin = ['Gross Margin']
    operating_margin = ['Operating Margin']
    ROE = ['ROE']

    # Fetch all calculation statements we need
    interest_expense = df.loc[df['Breakdown'] == 'Interest Expense'].values.tolist()[0][1:]
    net_income = df.loc[df['Breakdown'] == 'Net Income'].values.tolist()[0][1:]
    total_revenue = df.loc[df['Breakdown'] == 'Total Revenue'].values.tolist()[0][1:]
    stockholder_equity = df.loc[df['Breakdown'] == 'Stockholder Equity'].values.tolist()[0][1:]
    operating_income = df.loc[df['Breakdown'] == 'Operating Income'].values.tolist()[0][1:]
    gross_profit = df.loc[df['Breakdown'] == 'Gross Profit'].values.tolist()[0][1:]


    # Calculate interest coverage and append to the dataframe (we use net income as numerator
    # instead of using EBIT (earnings before interest and texas))
    interest_coverage += calculate_margin(net_income, interest_expense, False)
    df.loc[len(df)] = interest_coverage

    # Calculate net margin and append to the dataframe
    net_margin += calculate_margin(net_income, total_revenue, True)
    df.loc[len(df)] = net_margin

    # Calculate gross margin and append to the dataframe
    gross_margin += calculate_margin(gross_profit, total_revenue, True)
    df.loc[len(df)] = gross_margin

    # Calculate operating margin and append to the dataframe
    operating_margin += calculate_margin(operating_income, total_revenue, True)
    df.loc[len(df)] = operating_margin

    # Calculate ROE and append to the dataframe
    ROE += calculate_margin(net_income, stockholder_equity, True)
    df.loc[len(df)] = ROE

    return df


def drop_margin_statements(df: pd.DataFrame(), drop_titles: list) -> pd.DataFrame():
    # Remove some statements that are only for margin calculations
    for title in drop_titles:
        df = df.drop(df.index[df['Breakdown'] == title])
    df = df.reset_index(drop=True)

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
            df = add_margin_statements(df)

            # Drop titles that are only for margin calculation
            df = drop_margin_statements(df, config.drop_titles)

            # Store the dateframe in a specific sheet and named it according to its stock symbol
            df.to_excel(writer, sheet_name=stock_symbol, index=False)

    print(f"\nSuccessfully saved financial report!\n-> Path: {config.save_path}\n")
