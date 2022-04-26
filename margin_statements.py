import config
import pandas as pd


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

    # Get all titles
    all_title = df['Breakdown'].values.tolist()

    if 'Total Revenue' in all_title:
        total_revenue = df.loc[df['Breakdown'] == 'Total Revenue'].values.tolist()[0][1:]

        if 'Net Income' in all_title:
            net_income = df.loc[df['Breakdown'] == 'Net Income'].values.tolist()[0][1:]

            # Calculate net margin and append to the dataframe
            net_margin += calculate_margin(net_income, total_revenue, True)
            df.loc[len(df)] = net_margin

            if 'Interest Expense' in all_title:
                interest_expense = df.loc[df['Breakdown'] == 'Interest Expense'].values.tolist()[0][1:]

                # Calculate interest coverage and append to the dataframe (we use net income as numerator
                # instead of using EBIT (earnings before interest and texas))
                interest_coverage += calculate_margin(net_income, interest_expense, False)
                df.loc[len(df)] = interest_coverage

            if 'Stockholder Equity' in all_title:
                stockholder_equity = df.loc[df['Breakdown'] == 'Stockholder Equity'].values.tolist()[0][1:]

                # Calculate ROE and append to the dataframe
                ROE += calculate_margin(net_income, stockholder_equity, True)
                df.loc[len(df)] = ROE

        if 'Gross Profit' in all_title:
            gross_profit = df.loc[df['Breakdown'] == 'Gross Profit'].values.tolist()[0][1:]

            # Calculate gross margin and append to the dataframe
            gross_margin += calculate_margin(gross_profit, total_revenue, True)
            df.loc[len(df)] = gross_margin

        if 'Operating Income' in all_title:
            operating_income = df.loc[df['Breakdown'] == 'Operating Income'].values.tolist()[0][1:]

            # Calculate operating margin and append to the dataframe
            operating_margin += calculate_margin(operating_income, total_revenue, True)
            df.loc[len(df)] = operating_margin

    return df


def drop_margin_statements(df: pd.DataFrame()) -> pd.DataFrame():
    # Remove some statements that are only for margin calculations
    for title in config.drop_titles:
        df = df.drop(df.index[df['Breakdown'] == title])
    df = df.reset_index(drop=True)

    return df
