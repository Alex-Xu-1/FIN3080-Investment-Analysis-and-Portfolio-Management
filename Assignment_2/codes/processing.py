import pandas as pd
from pandas.tseries.offsets import DateOffset


# Renaming datasets columns
def renaming_columns(df, new_names):
    df = df.rename(columns=new_names)
    return df

                
# Create a new column "date_yq" specifiying the "year-quarter" information of each line in each dataset
def add_year_quarter_column(df, date_column_name, new_column_name):
    # Ensure the date column is in datetime format
    df[date_column_name] = pd.to_datetime(df[date_column_name])

    # Create the year-quarter string and assign it to the new column
    df[new_column_name] = (
        df[date_column_name].dt.year.astype(str)
        + "-q"
        + df[date_column_name].dt.quarter.astype(str)
    )
    return df


# Create a new column that is lagged by 3 months(a quarter) and specifies the "year-quarter" information of each line
def add_lagged_year_quarter_column(df, date_column_name, new_column_name):
    
    # Ensure the date column is in datetime format
    df[date_column_name] = pd.to_datetime(df[date_column_name])

    # Adjust dates to the previous quarter by subtracting 3 months
    df['Lagged_date_yq'] = df[date_column_name] - DateOffset(months=3)
    
    # Create the year-quarter string for the adjusted date and assign it to the new column
    df[new_column_name] = (
        df['Lagged_date_yq'].dt.year.astype(str)
        + "-q"
        + df['Lagged_date_yq'].dt.quarter.astype(str)
    )
    df.drop(columns=['Lagged_date_yq'], inplace=True) # delete the temporary column
    return df
    

# Iteratively merges a base DataFrame with a list of other DataFrames.
def merge_datasets(base_df, merge_list):
    merged_df = base_df
    for df, merge_cols in merge_list:
        merged_df = pd.merge(merged_df, df, on=merge_cols, how="left")
    return merged_df

# Filtering by percentile
def filter_by_percentile(df, column_name, lower_percentile=5, upper_percentile=95):
    lower_bound = df[column_name].quantile(lower_percentile / 100)
    upper_bound = df[column_name].quantile(upper_percentile / 100)
    filtered_df = df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]
    return filtered_df

def main():
# Read in the datasets

    monthly_stock_info = pd.read_csv(
        "/Users/admin/Desktop/Assignment_2/raw_data/monthly_Stock_Closing_Price_Return/monthly_Stock_Closing_Price_Return.csv"
    )
    
    net_asset_per_share = pd.read_csv(
        "/Users/admin/Desktop/Assignment_2/raw_data/Net_Assets_per_share/Net_Assets_per_share.csv"
    )
    
    stock_volatility = pd.read_csv(
        "/Users/admin/Desktop/Assignment_2/raw_data/daily_stock_volatility/daily_stock_volatility.csv"
    )
    
    roe = pd.read_csv(
        "/Users/admin/Desktop/Assignment_2/raw_data/quarterly_ROE/quarterly_ROE.csv"
    )


# Renaming datasets columns
   
    monthly_stock_info = renaming_columns(
        monthly_stock_info,
        {
            "Trdmnt": "Trade_Month",
            "Mclsprc": "Monthly_Closing_Price",
            "Mretnd": "Monthly_Returns",
        },
    )

    net_asset_per_share = renaming_columns(
        net_asset_per_share,
        {"F091001A": "NAPS",
         "Accper": "Reporting_Date"},
    )
    
    roe = renaming_columns(
        roe,
        {"F050504C": "ROE", 
         "Accper": "Reporting_Date"},
    )
    
    stock_volatility = renaming_columns(
        stock_volatility,
        {
         "Symbol": "Stkcd",
         "TradingDate": "Trade_Month",
        },
    )

# Converting the dates data to datetype
    monthly_stock_info["Trade_Month"] = pd.to_datetime(monthly_stock_info['Trade_Month'], format="mixed")
    net_asset_per_share["Reporting_Date"] = pd.to_datetime(net_asset_per_share['Reporting_Date'], format="mixed")
    roe["Reporting_Date"] = pd.to_datetime(roe['Reporting_Date'], format="mixed")
    


# Drop the rows with missing values & duplicated rows
    monthly_stock_info = monthly_stock_info.dropna().drop_duplicates()
    net_asset_per_share = net_asset_per_share.dropna().drop_duplicates()
    roe = roe.dropna().drop_duplicates()
    stock_volatility = stock_volatility.dropna().drop_duplicates()
    


# Create a new column "date_yq" specifiying the "year-quarter" information of each line in each dataset
    add_year_quarter_column(net_asset_per_share, "Reporting_Date", "date_yq")
    add_year_quarter_column(roe, "Reporting_Date", "date_yq")
    # note that the following dataset will be lagged for 1 quater for calculation purposes.
    add_lagged_year_quarter_column(monthly_stock_info, "Trade_Month", "date_yq") 

# drop the unnecessary rows with Typrep == "B" in datasets
    net_asset_per_share = net_asset_per_share[net_asset_per_share["Typrep"] != "B"]
    roe = roe[roe["Typrep"] != "B"]


# Drop the unnecessary columns & rows before merging
    net_asset_per_share = net_asset_per_share.drop(columns=["Typrep", "ShortName_EN", "Reporting_Date"])
    roe = roe.drop(columns=["Typrep", "ShortName_EN", "Reporting_Date"])

# Adjust the date of stock_volatility dataset to match the date of monthly_stock_info dataset
    stock_volatility["Trade_Month"] = "2010-12-01"
    

# Merging datasets
    # Set the merge_list containing merging information
    merge_list = [
        (net_asset_per_share, ["Stkcd", "date_yq"]),
        (roe, ["Stkcd", "date_yq"]),
    ]

    merged_dt = merge_datasets(monthly_stock_info, merge_list)

    
# Drop the rows with missing values in merged dataset
    merged_dt = merged_dt.dropna(subset=["NAPS"])
    
# Generate a new column for PB ratio
    merged_dt["PB_ratio"] = merged_dt["Monthly_Closing_Price"] / merged_dt["NAPS"]

    merged_dt = merged_dt.dropna(subset=["PB_ratio"])
    
# Filter the merged dataset by the 5th and 95th percentiles of the PB ratio
    merged_dt = filter_by_percentile(merged_dt, "PB_ratio", 5, 95)
    merged_dt = merged_dt.drop(columns=["NAPS", "Monthly_Closing_Price"])
   
# Save the processed raw datasets to new files
    monthly_stock_info.to_csv(
        "/Users/admin/Desktop/Assignment_2/processing/monthly_Stock_Closing_Price_Return_processed.csv",
        index=False,
    )
    net_asset_per_share.to_csv(
        "/Users/admin/Desktop/Assignment_2/processing/Net_Assets_per_share_processed.csv",
        index=False,
    )
    stock_volatility.to_csv(
        "/Users/admin/Desktop/Assignment_2/processing/daily_stock_volatility_processed.csv",
        index=False,
    )
    roe.to_csv(
        "/Users/admin/Desktop/Assignment_2/processing/quarterly_ROE_processed.csv",
        index=False,
    )
    stock_volatility.to_csv(
        "/Users/admin/Desktop/Assignment_2/processing/daily_stock_volatility_processed.csv",
        index=False,
    )
    
    
# Save the merged dataset to a new file
    merged_dt.to_csv(
        "/Users/admin/Desktop/Assignment_2/processing/PB_ratios.csv",
        index=False,
    )

    print("Processing is done!")


if __name__ == "__main__":
    main()
