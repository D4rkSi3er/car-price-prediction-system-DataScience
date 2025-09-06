import pandas as pd
from datetime import date

def clean_data(df):
    """
    Cleans the car dataset by handling missing values, removing duplicates, and renaming columns.
    """
    print("\nStep 2: Cleaning Data...")
    
    # Missing Values
    print("Checking for missing values...")
    print(df.isnull().sum())

    # Duplicates
    print(f"\nNumber of duplicate rows before cleaning: {df.duplicated().sum()}")
    df.drop_duplicates(inplace=True)
    print(f"Number of duplicate rows after cleaning: {df.duplicated().sum()}")

    # Rename
    df.rename(columns={
        'name': 'car_name',
        'km_driven': 'kms_driven',
        'fuel': 'fuel_type',
        'seller_type': 'seller_type',
        'transmission': 'transmission_type',
        'owner': 'owner_type'
    }, inplace=True)

    print("\nData cleaning step complete.")
    print("Columns after cleaning:", df.columns.tolist())
    
    return df

if __name__ == '__main__':
    try:
        raw_df = pd.read_csv('CAR DETAILS FROM CAR DEKHO.csv')
        cleaned_df = clean_data(raw_df.copy())
        
        # pipeline
        cleaned_df.to_csv('cleaned_car_data.csv', index=False)
        print("\nCleaned data saved to 'cleaned_car_data.csv'")

        print("\nCleaned DataFrame head:")
        print(cleaned_df.head())
    except FileNotFoundError:
        print("Error: 'CAR DETAILS FROM CAR DEKHO.csv' not found. Please ensure the file is in the same directory.")

