Car Price Prediction System with AI Insights

This project builds a machine learning model to predict the selling price of used cars and integrates Google's Gemini AI to provide an expert analysis of the valuation.
Project Overview

The project follows a standard data science workflow:

    Data Loading & Cleaning: Raw data is loaded and processed to handle duplicates and missing values.

    Exploratory Data Analysis (EDA): Key insights are discovered through visualizations.

    Feature Engineering: New, meaningful features like car_age are created, and categorical data is converted to a numerical format.

    Model Training: A RandomForestRegressor model is trained on the prepared data.

    Web Application: A user-friendly web app is built with Streamlit to make predictions and provide AI-generated analysis.

How to Run This Project
1. Prerequisites

You need to have Python installed. Then, install the required libraries:

pip install pandas scikit-learn seaborn matplotlib streamlit requests

2. Set Up Your Gemini API Key (Secure Method)

Your API key must be kept secret. Follow these steps:

    In the root folder of your project, create a new folder named .streamlit.

    Inside the .streamlit folder, create a new file named secrets.toml.

    Open secrets.toml and add the following line, replacing the placeholder with your actual Gemini API key:

    GEMINI_API_KEY = "YOUR_API_KEY_HERE"

The included .gitignore file will prevent this file from ever being uploaded to GitHub.
3. Run the Data Pipeline

Execute the scripts in order to process the data and train the model. This only needs to be done once.

python 01_data_loading.py
python 02_data_cleaning.py
python 03_eda_and_visualization.py
python 04_feature_engineering.py
python 05_model_training.py

This will generate the car_price_model.pkl file required by the application.
4. Run the Web Application

To start the user-friendly web interface, run the Streamlit app from your terminal:

streamlit run 07_app.py

Pushing to GitHub

Your project is now safe to push to a public GitHub repository. The .gitignore file will ensure your secrets, data files, and model file are not uploaded.
Deploying on Streamlit Community Cloud

    Push your project to a GitHub repository.

    Go to share.streamlit.io and sign in.

    Click "New app" and select your repository and the 07_app.py file.

    In the "Advanced settings," go to the "Secrets" tab.

    Paste the contents of your local secrets.toml file here.

    Click "Deploy!".
