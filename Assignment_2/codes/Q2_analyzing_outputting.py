import pandas as pd
import matplotlib.pyplot as plt

def main():
    initial_df = pd.read_csv("/Users/admin/Desktop/Assignment_2/processing/PB_ratios.csv")
    
    initial_df = initial_df.drop(columns=["ROE", "date_yq"])
    
    initial_df["Trade_Month"] = pd.to_datetime(initial_df["Trade_Month"], format = 'mixed')
    
    initial_df = initial_df.rename(columns={"Stkcd": "Stock_Code"})
    
    initial_df.to_csv("/Users/admin/Desktop/Assignment_2/processing/Q2_initial_dataset.csv", index=False)
    
    processing_df = initial_df
    # Sort data by Stock_Code and Trade_Month to ensure correct lagging
    processing_df.sort_values(by=['Stock_Code', 'Trade_Month'], inplace=True)

    # Create lagged_PB_ratios column
    processing_df['lagged_PB_ratio'] = processing_df.groupby('Stock_Code')['PB_ratio'].shift(1)
    
    processing_df = processing_df.dropna().drop_duplicates()
    
    processing_df.to_csv("/Users/admin/Desktop/Assignment_2/processing/Q2_processing_dataset.csv", index=False)
    
    # Assign decile groups based on 'lagged_PB_ratios'
    processing_df['Decile'] = processing_df.groupby('Trade_Month')['lagged_PB_ratio'].transform(
        lambda x: pd.qcut(x, 10, labels=False, duplicates='drop'))

    # Calculate monthly returns for each decile group
    monthly_returns = processing_df.groupby(['Trade_Month', 'Decile'])['Monthly_Returns'].mean().reset_index()

    # Calculate average returns for each decile group across all months
    average_returns = monthly_returns.groupby('Decile')['Monthly_Returns'].mean()

    # Visualize the average returns for the ten portfolios
    average_returns.plot(kind='bar')
    plt.xlabel('Portfolio Decile')
    plt.ylabel('Average Monthly Return')
    plt.title('Average Monthly Returns by Portfolio Decile (Jan. 2010 to Dec. 2023)')
    plt.show()

    
if __name__ == "__main__":
    main()