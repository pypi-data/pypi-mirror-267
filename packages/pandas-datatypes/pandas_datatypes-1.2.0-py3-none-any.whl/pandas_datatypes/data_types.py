import pandas as pd
import warnings

def infer_data_types(df: pd.DataFrame, fill_numeric_zeros: bool = True, date_format: str = None) -> dict:
    """
    Infer data types of columns in a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        fill_numeric_zeros (bool, optional): Whether to fill NaN values in numeric columns with zeros. Defaults to True.
        date_format (str, optional): Date format string to be used for parsing date columns. Defaults to None.

    Returns:
        dict: Dictionary containing column names as keys and inferred data types as values.
    """
    data_type_inference = {}

    def fill_zeros(col):
        if pd.api.types.is_numeric_dtype(col) and not pd.api.types.is_bool_dtype(col):
            if fill_numeric_zeros and col.any():
                col.fillna(0, inplace=True)
                if (col % 1 == 0).all():
                    return col.astype(int)
        return col
    temp_df = df.copy()
    temp_df = temp_df.apply(fill_zeros)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for column in df.columns:
            if not pd.api.types.is_any_real_numeric_dtype(temp_df[column]):
                try:
                    if date_format:
                        temp_df[column] = pd.to_datetime(temp_df[column], format=date_format)
                    else:
                        temp_df[column] = pd.to_datetime(temp_df[column])
                except:
                    pass

    for column in temp_df.columns:
        data_type_inference[column] = pd.api.types.infer_dtype(temp_df[column])

    return data_type_inference
