import pandas as pd

def load_data(filepath):
    
    print("Step 1: Loading Data...")
    try:
        df = pd.read_csv(filepath)
        print("Data loaded successfully!")
        print("First 5 rows of the dataset:")
        print(df.head())
        print("\nDataset Information:")
        df.info()
        print("\nDescriptive Statistics:")
        print(df.describe())
        return df
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None

if __name__ == '__main__':
    file_path = 'CAR DETAILS FROM CAR DEKHO.csv'
    car_data = load_data(file_path)

    if car_data is not None:
        print("\nData loading complete.")
