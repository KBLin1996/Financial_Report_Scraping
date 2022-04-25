import os
from datetime import date


# Report types
report_types = ['financials', 'balance-sheet', 'cash-flow']

# Indicators
key_indicators = ['Trailing P/E', 'Forward P/E', 'PEG Ratio (5 yr expected)', 'Price/Sales (ttm)',
                  'Price/Book (mrq)']
income_indicators = ['Total Revenue', 'Gross Profit', 'Operating Income',
                     'Net Income Common Stockholders', 'Basic EPS', 'Diluted EPS',
                     'Interest Expense']
balance_indicators = ['Total Equity Gross Minority Interest']
cash_flow_indicators = ['Operating Cash Flow', 'Capital Expenditure', 'Free Cash Flow']

indicators = income_indicators + balance_indicators + cash_flow_indicators

# Converting titles
convert_title_dict = {
                         'Net Income Common Stockholders': 'Net Income',
                         'Total Equity Gross Minority Interest': 'Stockholder Equity'
                     }

# Drop titles that are for margin calculation
drop_titles = ['Interest Expense']

# Stock symbols we traced
stock_symbols = ['AAPL', 'AMD', 'GOOGL']

# Save path using today's date as title
today = date.today()
today = today.strftime("%Y-%m-%d")

save_path = f"{os.getcwd()}/{today}_financial_report.xlsx"
