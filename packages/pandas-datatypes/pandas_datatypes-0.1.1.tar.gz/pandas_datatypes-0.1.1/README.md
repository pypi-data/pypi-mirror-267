# pandas_datatypes

## infer_data_types

![GitHub](https://img.shields.io/github/license/yourusername/infer_data_types)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/yourusername/infer_data_types)

A Python function for inferring data types of columns in a pandas DataFrame.

## Overview

`infer_data_types` is a utility function designed to assist in the process of inferring data types of columns within a pandas DataFrame. It offers functionality to handle numeric columns with NaN values by optionally filling them with zeros, and it can automatically convert columns to datetime objects where appropriate.

## Usage

```python
import pandas as pd
from infer_data_types import infer_data_types

# Create a DataFrame
data = {
    'A': [1, 2, 3],
    'B': ['2022-01-01', '2022-02-01', '2022-03-01'],
    'C': [4.0, None, 6.0],
}

df = pd.DataFrame(data)

# Infer data types
data_types = infer_data_types(df)

print(data_types)
```
# Function Description

```
def infer_data_types(df: pd.DataFrame, fill_numeric_zeros: bool = True) -> dict:
```
 
    Infer data types of columns in a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        fill_numeric_zeros (bool, optional): Whether to fill NaN values in numeric columns with zeros. Defaults to True.

    Returns:
        dict: Dictionary containing column names as keys and inferred data types as values.


df: Input DataFrame for which data types are to be inferred.

fill_numeric_zeros: Optional boolean parameter to indicate whether to fill NaN values in numeric columns with zeros. Defaults to True.

Returns a dictionary containing column names as keys and inferred data types as values.