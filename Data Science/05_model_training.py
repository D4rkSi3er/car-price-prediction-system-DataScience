import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import pickle

def train_model():
    """
    Loads processed data, splits it, trains a RandomForestRegressor model,
    evaluates it, and saves the trained model.
    """
    print("\nStep 5: Training the Machine Learning Model...")
    
    try:
        df = pd.read_csv('processed_car_data.csv')
    except FileNotFoundError:
        print("Error: 'processed_car_data.csv' not found.")
        print("Please run '04_feature_engineering.py' first to generate it.")
        return

    # X and y separation
    X = df.drop('selling_price', axis=1)
    y = df['selling_price']

    # training sets 
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Data split into training ({X_train.shape[0]} rows) and testing ({X_test.shape[0]} rows) sets.")

    # RandomForest 
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    print("Model training complete.")

    # Evaluating
    print("\nEvaluating model performance on the test set")
    y_pred = model.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"R-squared (R2) Score: {r2:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

    # saved model
    model_data = {
        'model': model,
        'columns': X.columns.tolist()
    }
    with open('car_price_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("\nTrained model and column list saved to 'car_price_model.pkl'.")

if __name__ == '__main__':
    train_model()
