import pandas as pd
import numpy as np

def clean_data(input_path, output_path):
    """Clean the superstore dataset"""
    
    # Load the data
    df = pd.read_csv(input_path, encoding='latin1')
    
    # 1. Check dataset structure
    print("Dataset Info:")
    print(df.info())
    print(f"\nShape: {df.shape}")
    
    # 2. Handle missing values
    print(f"\nMissing values before:\n{df.isnull().sum()}")
    df = df.dropna()
    
    # 3. Remove duplicates
    print(f"\nDuplicates found: {df.duplicated().sum()}")
    df = df.drop_duplicates()
    
    # 4. Convert dates to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    # 5. Standardize category names (title case)
    categorical_cols = ['Category', 'Sub-Category', 'Region', 'State', 'City']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].str.title()
    
    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f"\n✅ Cleaned data saved to {output_path}")
    print(f"Final shape: {df.shape}")
    
    return df

if __name__ == "__main__":
    clean_data('data/Superstore.csv', 'data/cleaned_superstore.csv')