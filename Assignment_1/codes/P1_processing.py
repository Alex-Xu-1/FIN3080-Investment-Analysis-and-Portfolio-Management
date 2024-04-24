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


def main():
# Read in the datasets
    eps_net_assets = pd.read_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/raw_data/EPS_&_Net_Assets_per_Share/EPS_&_Net_Assets_per_Share.csv"
    )
    
    establishment_date_market_type = pd.read_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/raw_data/Establishment_Date_&_Market_Type/Establishment_Date_&_Market_Type.csv"
    )

    monthly_stock_info = pd.read_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/raw_data/Monthly_Stock_Price_&_Returns_&_Market_Value_of_Tradable_shares/Monthly_Stock_Price_&_Returns_&_Market_Value_of_Tradable_shares.csv"
    )

    quarterly_TA_TL = pd.read_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/raw_data/Quarterly_TA&TL/Quarterly_TA&TL.csv"
    )
    
    RD_expenses = pd.read_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/raw_data/R&D_Expenses/R&D_Expenses.csv"
    )
    
    roa_roe = pd.read_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/raw_data/ROA_&_ROE/ROA_&_ROE.csv"
    )
    


# Renaming datasets columns
    eps_net_assets = renaming_columns(
        eps_net_assets,
        {
            "Accper": "Date_of_Statement",
            "F090101B": "EPS",
            "F091001A": "Net_Assets_per_Share",
        },
    )
    
    establishment_date_market_type = renaming_columns(
        establishment_date_market_type,
        {"Estbdt": "Establishment_Date", "Markettype": "Market_Type"},
    )
    # Market_Type: 1=SSE A share market (excluding STAR Market); 2= SSE B share market; 4= SZSE A share market (excluding ChiNext); 8= SZSE B share market; 16= ChiNext; 32= STAR Market; 64= BSE A share market;
    
    monthly_stock_info = renaming_columns(
        monthly_stock_info,
        {
            "Trdmnt": "Trade_Month",
            "Mclsprc": "Monthly_Closing_Price",
            "Msmvosd": "MktVal_Tradable_Shares",
            "Mretwd": "Monthly_Returns",
        },
    )

    quarterly_TA_TL = renaming_columns(
        quarterly_TA_TL,
        {
            "Accper": "Reporting_Date",
            "A001000000": "Total_Assets",
            "A002000000": "Total_Liabilities",
        },
    )

    RD_expenses = renaming_columns(
        RD_expenses, {"Accper": "Reporting_Date", "B001216000": "R&D_Expenses"}
    )

    roa_roe = renaming_columns(
        roa_roe, {"Accper": "Reporting_Date", "F050201B": "ROA", "F050501B": "ROE"}
    )


# Converting the dates data to datetype
    eps_net_assets["Date_of_Statement"] = pd.to_datetime(eps_net_assets['Date_of_Statement'], format="mixed")
    establishment_date_market_type["Establishment_Date"] = pd.to_datetime(establishment_date_market_type['Establishment_Date'], format="mixed")
    monthly_stock_info["Trade_Month"] = pd.to_datetime(monthly_stock_info['Trade_Month'], format="mixed")
    quarterly_TA_TL["Reporting_Date"] = pd.to_datetime(quarterly_TA_TL['Reporting_Date'], format="mixed")
    RD_expenses["Reporting_Date"] = pd.to_datetime(RD_expenses['Reporting_Date'], format="mixed")
    roa_roe["Reporting_Date"] = pd.to_datetime(roa_roe['Reporting_Date'], format="mixed")


# Drop the rows with missing values & duplicated rows
    eps_net_assets = eps_net_assets.dropna().drop_duplicates()
    establishment_date_market_type = (
        establishment_date_market_type.dropna().drop_duplicates()
    )
    monthly_stock_info = monthly_stock_info.dropna().drop_duplicates()
    quarterly_TA_TL = quarterly_TA_TL.dropna().drop_duplicates()
    RD_expenses = RD_expenses.dropna().drop_duplicates()
    roa_roe = roa_roe.dropna().drop_duplicates()
    

# Drop the rows with parent statements
    eps_net_assets = eps_net_assets.drop(
        eps_net_assets[eps_net_assets["Typrep"] == "B"].index
    )
    quarterly_TA_TL = quarterly_TA_TL.drop(
        quarterly_TA_TL[quarterly_TA_TL["Typrep"] == "B"].index
    )
    RD_expenses = RD_expenses.drop(RD_expenses[RD_expenses["Typrep"] == "B"].index)
    roa_roe = roa_roe.drop(roa_roe[roa_roe["Typrep"] == "B"].index)


# Create a new column "date_yq" specifiying the "year-quarter" information of each line in each dataset
    add_year_quarter_column(eps_net_assets, "Date_of_Statement", "date_yq")
    add_year_quarter_column(establishment_date_market_type, "Establishment_Date", "date_yq_establish")  
    add_year_quarter_column(quarterly_TA_TL, "Reporting_Date", "date_yq")
    add_year_quarter_column(RD_expenses, "Reporting_Date", "date_yq")
    add_year_quarter_column(roa_roe, "Reporting_Date", "date_yq")
    # note that the following dataset will be lagged for 1 quater for calculation purposes.
    add_lagged_year_quarter_column(monthly_stock_info, "Trade_Month", "date_yq") 

# Solving an issue with recording error in the dataset "quarterly_TA_TL"
    quarterly_TA_TL = quarterly_TA_TL[
        ~(
            (quarterly_TA_TL["Reporting_Date"].dt.month == 1)
            & (quarterly_TA_TL["Reporting_Date"].dt.day == 1)
        )
    ]


# Keeping rows that are not on the first day of any year except for "2018-01-01" (after noticing some issues with wrong data recordings in this dataset)
    RD_expenses = RD_expenses[
        ~(
            (RD_expenses["Reporting_Date"].dt.month == 1)
            & (RD_expenses["Reporting_Date"].dt.day == 1)
            & (RD_expenses["Reporting_Date"].dt.year != 2018)
        )
    ]


# Drop the unnecessary columns & rows before merging
    eps_net_assets = eps_net_assets.drop(columns=["Typrep", "Date_of_Statement"])
    establishment_date_market_type = establishment_date_market_type.drop(
        columns=["Listdt", "Stknme_en"]
    )
    monthly_stock_info = monthly_stock_info.drop(columns=["MktVal_Tradable_Shares"])
    quarterly_TA_TL = quarterly_TA_TL.drop(
        columns=["Typrep", "ShortName_EN", "Reporting_Date"]
    )
    RD_expenses = RD_expenses.drop(columns=["Typrep", "ShortName_EN", "Reporting_Date"])
    roa_roe = roa_roe.drop(columns=["Typrep", "ShortName_EN", "Reporting_Date"])


# Merging datasets
    # Set the merge_list containing merging information
    merge_list = [
        (monthly_stock_info, ["Stkcd", "date_yq"]),
        (establishment_date_market_type, ["Stkcd"]),
        (quarterly_TA_TL, ["Stkcd", "date_yq"]),
        (RD_expenses, ["Stkcd", "date_yq"]),
        (roa_roe, ["Stkcd", "date_yq"]),
    ]

    merged_dt = merge_datasets(eps_net_assets, merge_list)

   
# Drop the rows with stocks that belong to B share market, where "Market_Type" is 2==SSE B share market or 8==SZSE B share market, thus only considering A share market stocks
    merged_dt = merged_dt.drop(merged_dt[merged_dt["Market_Type"].isin([2, 8])].index)

# Drop the rows with missing values in Monthly_Stock_Info
    merged_dt = merged_dt.dropna(subset=["Monthly_Closing_Price", "Monthly_Returns"])
    
# Save the processed raw datasets to new files
    eps_net_assets.to_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/processing/EPS_&_Net_Assets_per_Share_processed.csv",
        index=False,
    )
    establishment_date_market_type.to_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/processing/Establishment_Date_&_Market_Type_processed.csv",
        index=False,
    )
    monthly_stock_info.to_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/processing/Monthly_Stock_Info_processed.csv",
        index=False,
    )
    quarterly_TA_TL.to_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/processing/Quarterly_TA_TL_processed.csv",
        index=False,
    )
    RD_expenses.to_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/processing/RD_Expenses_processed.csv",
        index=False,
    )
    roa_roe.to_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/processing/ROA_ROE_processed.csv",
        index=False,
    )

# Save the merged dataset to a new file
    merged_dt.to_csv(
        "/Users/admin/Desktop/FIN3080_Assignment_1/Python_format_general-csv/processing/Merged_Dataset.csv",
        index=False,
    )

    print("Processing is done!")


if __name__ == "__main__":
    main()
