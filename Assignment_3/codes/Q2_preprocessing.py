import pandas as pd


weekly_returns = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/raw_data/weekly_returns_with_markettype/TRD_Week.csv')

#filter out the markettype 1 and 4 for main board stocks
weekly_returns = weekly_returns[weekly_returns['Markettype'].isin([1, 4])]

weekly_returns.drop(columns=['Markettype'], inplace=True)

#drop the rows with missing values in the column "Wretnd"
weekly_returns.dropna(subset=['Wretnd'], inplace=True)

#drop the rows with Wretnd == 0.0
weekly_returns = weekly_returns[weekly_returns['Wretnd'] != 0.0]

#calculated weekly market return: grouping the data by Trdwnt and calculate the mean of Wretnd, then store the mkt_return into a new dataset.
weekly_market_returns = weekly_returns.groupby('Trdwnt')['Wretnd'].mean().reset_index()

weekly_risk_free_rate = pd.read_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/raw_data/weekly_risk_free_rate.csv')

#renaming the columns
weekly_market_returns.columns = ['year_week', 'weekly_mkt_return']
weekly_risk_free_rate.columns = ['trading_date', 'weekly_rf_rate']

#convert the trading_week to year-week datetime format
weekly_risk_free_rate['trading_date'] = pd.to_datetime(weekly_risk_free_rate['trading_date'], format='mixed')
weekly_risk_free_rate['year_week'] = weekly_risk_free_rate['trading_date'].dt.strftime('%G-%V')

 

weekly_returns.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/processed_weekly_returns.csv', index=False)
weekly_market_returns.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/weekly_market_returns.csv', index=False)
weekly_risk_free_rate.to_csv('/Users/admin/Desktop/FIN3080_Assignment_3/Python/processed_data/processed_weekly_risk_free_rate.csv', index=False)
print("Processing completed.")