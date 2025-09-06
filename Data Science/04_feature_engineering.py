import pandas as pd
from datetime import date
import os

def engineer_features(df):
    """
    Handels Exceptions and performs feature engineering on the cleaned car dataset.
    """
    print("\nStep 4: Performing Feature Engineering...")

    rename_map = {
        'fuel': 'fuel_type',
        'transmission': 'transmission_type',
        'owner': 'owner_type'
    }
    df.rename(columns=rename_map, inplace=True, errors='ignore')
    print("Ensured consistent column names for feature engineering.")


    current_year = date.today().year
    df['car_age'] = current_year - df['year']
    print("Created 'car_age' feature.")

    # Encodin 
    columns_to_drop = ['car_name', 'year']
    final_df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # one-hot encoding
    try:
        # matches consistent names we just ensured.
        final_df = pd.get_dummies(final_df, columns=['fuel_type', 'seller_type', 'transmission_type', 'owner_type'], drop_first=True)
        print("One-hot encoded categorical features.")
    except KeyError as e:
        print(f"Error during one-hot encoding: {e}.")
        print("This may happen if the input CSV is missing one of the expected categorical columns.")
        return None

    print("\nFeature engineering step complete.")
    print("Columns after feature engineering:", final_df.columns.tolist())
    
    return final_df

if __name__ == '__main__':
    try:
        cleaned_df = pd.read_csv('cleaned_car_data.csv')
        featured_df = engineer_features(cleaned_df)
        if featured_df is not None:
            print("\nDataFrame ready for modeling (head):")
            print(featured_df.head())
            featured_df.to_csv('processed_car_data.csv', index=False)
            print("\nSaved processed data to 'processed_car_data.csv'")
    except FileNotFoundError:
        print("Error: 'cleaned_car_data.csv' not found. Please run '02_data_cleaning.py' first.")

