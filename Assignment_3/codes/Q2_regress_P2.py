import pandas as pd
import statsmodels.api as sm

P1_results = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P1_regression_result_1.csv')
P2 = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P2.csv')

P1_results.drop(columns=['Alpha', 'R-squared'], inplace=True)

#assign decile groups to each stock based on beta, the highest beta is assigned to decile 10 and the lowest beta is assigned to decile 1
P1_results['Decile'] = pd.qcut(P1_results['Beta'], 10, labels=False) + 1

P1_results.sort_values(by='Beta', inplace=True)

P2.drop(columns=['weekly_stock_return', 'weekly_mkt_return', 'weekly_rf_rate'], inplace=True)

#merge the two datasets
P2_results = pd.merge(P2, P1_results, on='Stkcd')

#calculate the weekly portfolio return rp_rf using simple average on each decile group's ri_rf, and store the calculated rp_rf into the new column 'rp_rf'
P2_results['rp_rf'] = P2_results.groupby(['year_week', 'Decile'])['ri_rf'].transform('mean')

#regress rp_rf on rm_rf to get the alpha and beta for each decile group
decile_results = []

decile_number = P2_results['Decile'].unique()

for decile in decile_number:
    temp_df = P2_results[P2_results['Decile'] == decile]
    
    X = sm.add_constant(temp_df['rm_rf'])
    y = temp_df['rp_rf']
    
    if len(temp_df) > 1:
        model = sm.OLS(y, X, missing='drop')
        results = model.fit()
        
        decile_results.append({
            'Decile': decile,
            'Alpha': results.params.get('const', 0),
            'Alpha t-value': results.tvalues.get('const', 0),
            'Alpha p-value': results.pvalues.get('const', 1),  # Default to 1 (non-significant) if not available
            'Beta': results.params.get('rm_rf', 0),
            'Beta t-value': results.tvalues.get('rm_rf', 0),
            'Beta p-value': results.pvalues.get('rm_rf', 1),
            'R-squared': results.rsquared,
        })
    else:
        # Provide defaults if regression is not possible
        decile_results.append({
            'Decile': decile,
            'Alpha': None,
            'Alpha t-value': None,
            'Alpha p-value': None,
            'Beta': None,
            'Beta t-value': None,
            'Beta p-value': None,
            'R-squared': None,
        })

decile_results_df = pd.DataFrame(decile_results)
decile_results_df.sort_values(by='Decile', inplace=True)
decile_results_df['Beta p-value'] = decile_results_df['Beta p-value'].apply(lambda x: f"{x:.6e}")

#print out the results in a table format
print(decile_results_df)

P1_results.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P1_temp.csv', index=False)
P2_results.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P2_temp.csv', index=False)
decile_results_df.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P2_regression_result.csv', index=False)
print("Processing completed.")  
