import pandas as pd


def one_hot_encoding_selected(data, columns):
    """
    Perform one-hot encoding on selected columns while retaining numeric values.

    Parameters:
    data (DataFrame): The input DataFrame.
    columns (list): List of column names to one-hot encode.

    Returns:
    list: List of lists with one-hot encoded columns.
    """
    # Copy the original DataFrame
    encoded_data = data.copy()
    
    # Iterate through selected columns
    for column in columns:
        # Check if column exists and is categorical
        if column in data.columns and data[column].dtype == 'object':
            # Perform one-hot encoding
            encoded_column = pd.get_dummies(data[column], prefix=column)
            # Drop original column and concatenate one-hot encoded columns
            encoded_data = pd.concat([encoded_data.drop(column, axis=1), encoded_column], axis=1)
    
    # Convert DataFrame to list of lists
    encoded_list = encoded_data.values.tolist()
    
    return encoded_list

