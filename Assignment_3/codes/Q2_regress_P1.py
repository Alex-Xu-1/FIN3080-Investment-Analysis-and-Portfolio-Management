import pandas as pd
import statsmodels.api as sm

# Load the dataset
P1 = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P1.csv')

# Get unique stock codes
stock_codes = P1['Stkcd'].unique()

# List to store regression results
regression_results = []

for code in stock_codes:
    # Filter the DataFrame for the current stock code
    temp_df = P1[P1['Stkcd'] == code]
    
    # Add a constant term for the intercept
    X = sm.add_constant(temp_df['weekly_mkt_return'])
    y = temp_df['weekly_stock_return']
    
    # Perform the regression
    model = sm.OLS(y, X, missing='drop')  # 'drop' will drop all NaN values
    results = model.fit()
    
    # Store results as a dictionary in the list
    regression_results.append({
        'Stock Code': code,
        'Alpha': results.params['const'],
        'Beta': results.params['weekly_mkt_return'],
        #'T-values': str(results.tvalues),
        #'P-values': str(results.pvalues),
        'R-squared': results.rsquared
    })

# Convert the list of dictionaries to a DataFrame
results_df = pd.DataFrame(regression_results)

# Save the DataFrame to a CSV file
results_df.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P1_regression_result.csv', index=False)

# Optional: Print or view the DataFrame
print(results_df.head())
print("Processing completed.")