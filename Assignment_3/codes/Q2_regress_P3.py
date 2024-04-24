import pandas as pd
import statsmodels.api as sm

P1_results = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P1_temp.csv')
P2_results = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P2_regression_result.csv')
P3 = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/P3.csv')

#drop unnecessary columns
P1_results.drop(columns=['Beta'], inplace=True)

#merge the P1_results with P3 on Stkcd
merged = pd.merge(P3, P1_results, on='Stkcd')
merged.dropna()

#drop columns
merged.drop(columns=['weekly_stock_return', 'weekly_mkt_return', 'weekly_rf_rate', 'rm_rf'], inplace=True)
P2_results = P2_results[['Decile', 'Beta']]

merged = pd.merge(merged, P2_results, on='Decile')

#calculated the weekly portfolio return rp_rf using simple average on each decile group's ri_rf, and store the calculated rp_rf into the new column 'rp_rf'
merged['rp_rf'] = merged.groupby(['Decile'])['ri_rf'].transform('mean')

#delete columns
merged.drop(columns=['ri_rf', 'Stkcd', 'year_week'], inplace=True)

merged.drop_duplicates(inplace=True)

merged.sort_values('Decile', inplace=True)

#regress rp_rf on Beta
decile_results = []

X = sm.add_constant(merged['Beta'])
y = merged['rp_rf']
model = sm.OLS(y, X, missing='drop')
results = model.fit()
decile_results.append({
    'Gamma_0': results.params.get('const', 0),
    'Gamma_1': results.params.get('Beta', 0),
    't-value_Gamma_0': results.tvalues.get('const', 0),
    't-value_Gamma_1': results.tvalues.get('Beta', 0),
    'R-squared': results.rsquared,
    'F-statistic': results.fvalue,
    'P-value': results.f_pvalue,
})
    
decile_results_df = pd.DataFrame(decile_results)
print(decile_results_df)

merged.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/merged.csv', index=False)
decile_results_df.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/result_for_Table_3.csv', index=False) 
print("Processing completed.")


