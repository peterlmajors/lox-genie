
import pandas as pd
import probablepeople as pp

# Additional Functionality by Inner Merge More Transparent by Printing Mismatches
def merge_and_print_unmatched(df1, df2, left_key, right_key):
    
    # Perform inner merge and find unmatched keys
    merged_df = pd.merge(df1, df2, left_on=left_key, right_on=right_key, how='inner')
    unmatched_left = set(df1[left_key]) - set(merged_df[left_key])
    unmatched_right = set(df2[right_key]) - set(merged_df[right_key])
    
    # Print unmatched keys
    print(f"Unmatched keys from left dataframe: {unmatched_left}")
    print(f"Unmatched keys from right dataframe: {unmatched_right}")
    
    return merged_df

# Examine Partial Names When Mismatches Occur in DataFrames
def partial_name_print_matches(partial_name: str, df1: pd.DataFrame, df2: pd.DataFrame, df1_col: str, df2_col: str):
    
    print('Dataframe 1.', df1[df1[df1_col].str.contains(partial_name, na = False)][df1_col])
    print('Dataframe 2.', df2[df2[df2_col].str.contains(partial_name, na = False)][df2_col])
    
# Extract First and Last Name Only
def first_last_name(name: str): 
    parsed_name = pp.parse(name)
    return ' '.join(component[0] for component in parsed_name if component[1] in ['GivenName', 'Surname'])