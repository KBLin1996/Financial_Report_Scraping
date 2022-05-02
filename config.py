import os
from datetime import date


# Save path using today's date as title
today = date.today()
today = today.strftime("%Y-%m-%d")

save_path = f"{os.getcwd()}/{today}_financial_report.xlsx"

# Report types
report_types = ['financials', 'balance-sheet', 'cash-flow']

# Indicators
key_indicators = ['Trailing P/E', 'Forward P/E', 'PEG Ratio (5 yr expected)', 'Price/Sales (ttm)',
                  'Price/Book (mrq)']
income_indicators = ['Total Revenue', 'Gross Profit', 'Operating Income',
                     'Net Income Common Stockholders', 'Basic EPS', 'Diluted EPS',
                     'Interest Expense']
balance_indicators = ['Total Assets', 'Total Liabilities Net Minority Interest', 'Total Equity Gross Minority Interest']
cash_flow_indicators = ['Operating Cash Flow', 'Capital Expenditure', 'Free Cash Flow']

indicators = income_indicators + balance_indicators + cash_flow_indicators

# Converting titles
convert_title_dict = {
                         'Net Income Common Stockholders': 'Net Income',
                         'Total Equity Gross Minority Interest': 'Stockholder Equity'
                     }

# Drop titles that are for margin calculation
drop_titles = ['Total Assets', 'Total Liabilities Net Minority Interest', 'Stockholder Equity', 'Interest Expense']

# Stock symbols we traced
stock_symbols = ['AAPL', 'GOOGL', 'NVDA', 'AMD', 'AMZN', 'MSFT', 'FB', 'TSLA', 'PYPL', 'SHOP', 'JPM',
                 'VZ', 'SBUX', 'CRM', 'ROKU', 'UAA', 'SNOW']

# Explanation dictionary
# Reference: https://george-dewi.com/financial-report-analysis/
explanation = {
                  'Total Revenue': '公司尚未扣除任何費用的總收入。',
                  'Gross Profit': '毛利 = 總營收 - 營業成本',
                  'Operating Income': '公司透過商業活動所獲得的收入，通常是提供產品及服務而來。',
                  'Net Income': '是評估公司獲利能力的關鍵。',
                  'Basic EPS': '是公司的獲利指標，而通常EPS與股價也會有非常大的關連性。',
                  'Diluted EPS': '許多上市公司會向員工發放股票選擇權、認股權證，當成對員工激勵或長期留才一種方式，\
                  這樣看似短期減少公司薪資支出成本，但長期而言會增加了普通股的數量、稀釋每股獲利。\
                  所以如果發現企業這類衍生性商品發行較多，計算獲利能力時最好是使用稀釋EPS，會比EPS更加有參考價值準確。',
                  'Stockholder Equity': '淨資產(股東權益) = 資產 - 債務(非股東處借來的資金)',
                  'Net Asset Ratio': '淨資產比例 = 淨資產 / 總資產 (> 50% 安全, < 10% 危險)',
                  'Operating Cash Flow': '公司生產營運所帶來的現金流入和流出的數值，包括所有折舊與攤提。',
                  'Capital Expenditure': '購入未來可替公司增加經濟效益的固定資產。如廠房、機器設備等。',
                  'Free Cash Flow': '是公司可自由運用的現金流，衡量公司手上持有現金的狀況。',
                  'Net Margin': '公司從總營收中計算淨收入的比例',
                  'Interest Coverage': '衡量一間公司支付負債利息的能力，如果數值愈高就代表企業還錢的能力越好。',
                  'ROE': 'Return on Equity: 公司利用資產淨值產生利益的能力，也就是公司替股東賺錢的能力。',
                  'Gross Margin': '代表產品的成本與總收入的關係 => 一項產品扣掉直接成本，可從售價獲利幾%',
                  'Operating Margin': '營業利率則是營業利潤與總營收的關係 => 一項產品扣掉所有成本，可從售價獲利幾%'
              }
