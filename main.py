# Self-defined files
import utils
import config
import fetch_reports
import margin_statements

import pandas as pd


if __name__ == '__main__':
    with pd.ExcelWriter(config.save_path, engine='openpyxl') as writer:
        for stock_symbol in config.stock_symbols:
            # Fetch all given stock symbol's reports in HTML format from Yahoo finanace and extract the
            # indicators we want from them
            df = fetch_reports.organize_reports(stock_symbol)

            # Filter all nan values and replace some statements' titles
            df = utils.clean_dataframe(df)

            # Add margin statements into the dataframe
            df = margin_statements.add_margin_statements(df)

            # Drop titles that are only for margin calculation
            df = margin_statements.drop_margin_statements(df)

            # Store the dateframe in a specific sheet and named it according to its stock symbol
            df.to_excel(writer, sheet_name=stock_symbol, index=False)

            print(f"Done scraping {stock_symbol}")

    print(f"\nSuccessfully saved financial all report!\n-> Path: {config.save_path}\n")