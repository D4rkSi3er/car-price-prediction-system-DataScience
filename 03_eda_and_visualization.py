import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import date

def perform_eda(df):
    """
    Performs EDA and Data Visualization on the cleaned car dataset.
    """
    print("\nStep 3: Performing Exploratory Data Analysis (EDA)...")
    
    if not os.path.exists('visualizations'):
        os.makedirs('visualizations')
    
    current_year = date.today().year
    df['car_age'] = current_year - df['year']

    # Price Dist
    plt.figure(figsize=(10, 6))
    sns.histplot(df['selling_price'], kde=True, bins=50)
    plt.title('Distribution of Selling Price')
    plt.xlabel('Selling Price')
    plt.ylabel('Frequency')
    plt.savefig('visualizations/01_price_distribution.png')
    plt.close()
    print("Saved plot: 01_price_distribution.png")

    # Colrelation Heatmap
    plt.figure(figsize=(12, 8))
    numeric_cols = df.select_dtypes(include=['number'])
    sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix of Numerical Features')
    plt.savefig('visualizations/02_correlation_heatmap.png')
    plt.close()
    print("Saved plot: 02_correlation_heatmap.png")

    # Feature vs Price
    categorical_features = ['fuel_type', 'seller_type', 'transmission_type', 'owner_type']
    for i, feature in enumerate(categorical_features):
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=feature, y='selling_price', data=df)
        plt.title(f'Selling Price vs. {feature}')
        plt.xticks(rotation=45)
        plt.savefig(f'visualizations/03_{i+1}_{feature}_vs_price.png')
        plt.close()
        print(f"Saved plot: 03_{i+1}_{feature}_vs_price.png")

    print("\nEDA and visualization step complete. Check the 'visualizations' folder.")

if __name__ == '__main__':
    try:
        cleaned_df = pd.read_csv('cleaned_car_data.csv')
        perform_eda(cleaned_df)
    except FileNotFoundError:
        print("Error: 'cleaned_car_data.csv' not found. Please run '02_data_cleaning.py' first to generate it.")

