import pandas as pd

# Load cleaned data
df = pd.read_csv('data/cleaned_superstore.csv')

# 1. Extract time features
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Quarter'] = df['Order Date'].dt.quarter
df['Order Day'] = df['Order Date'].dt.day
df['Order Day of Week'] = df['Order Date'].dt.day_name()

# 2. Calculate Profit Margin
df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100

# 3. Create Shipping Duration
df['Shipping Duration'] = (df['Ship Date'] - df['Order Date']).dt.days

# 4. Create Sales Category (Low, Medium, High)
def categorize_sales(sales):
    if sales < 100:
        return 'Low'
    elif sales < 500:
        return 'Medium'
    else:
        return 'High'

df['Sales Category'] = df['Sales'].apply(categorize_sales)

# Save the enhanced dataset
df.to_csv('data/final_superstore.csv', index=False)
print("Data manipulation complete!")