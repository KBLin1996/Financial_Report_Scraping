import config
import pandas as pd


def merge_explanation(df) -> pd.DataFrame():
    explanation_list = list()
    explanation_dict = config.explanation

    all_title = df['Breakdown'].values.tolist()
    for title in all_title:
        if title in explanation_dict.keys():
            explanation_list.append(explanation_dict[title])

    df['Explanation'] = explanation_list
    
    return df
