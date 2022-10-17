# Financial_Report_Scraping

Description: Scrape Financial Reports (financials, balance sheet, cash flow) from Yahoo Finance.

Testing OS: ```M1 Macbook Pro```

### How to execute?
```
python main.py
```

### Important Notes:
1. Please download the corresponding chromedriver at https://chromedriver.chromium.org/downloads and place it under this local repository.

2. We are solving the error message showing in the image below by following three instructions. (Reference: https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de)
    1. Open terminal.
    2. Navigate to the path where chromedriver is located (under the local repository in this example).
    3. Execute the following command: ```xattr -d com.apple.quarantine <name-of-executable>```

<img src="cannot_open_chromedrive.png" alt="Cannot Open chromedrive on Macbook" width="200">
