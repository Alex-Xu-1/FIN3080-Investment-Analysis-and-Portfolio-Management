import pandas as pd

weekly_market_returns = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/weekly_market_returns.csv')
weekly_rf_rate = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/processed_weekly_risk_free_rate.csv')
processed_weekly_returns = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/processed_weekly_returns.csv')

#renaming
processed_weekly_returns.columns = ['Stkcd', 'year_week', 'weekly_stock_return']

#merge the weekly_market_returns and weekly_rf_rate
merged_weekly_market_rf = pd.merge(weekly_market_returns, weekly_rf_rate, on='year_week')

#delete the column "trading_date" in the merged_weekly_market_rf
merged_weekly_market_rf.drop(columns=['trading_date'], inplace=True)


merged_weekly_market_rf.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/merged_weekly_market_rf.csv', index=False)
processed_weekly_returns.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/processed_weekly_returns.csv', index=False)

print("Processing completed.")