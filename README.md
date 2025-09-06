🚗 Car Price Prediction System with AI Insights

A comprehensive machine learning project that predicts the selling price of used cars and leverages Google's Gemini AI to provide users with expert valuation analysis.
✨ Live Demo

(Link to your deployed Streamlit App will go here)
🎬 Application Preview

(A GIF or screenshot of your final Streamlit application in action would be perfect here!)
📋 Table of Contents

    Project Overview

    Features

    Technologies Used

    Setup and Installation

    Usage

    Project Structure

    Deployment

    License

🌐 Project Overview

This project demonstrates a complete end-to-end data science workflow. It begins with a raw dataset of used car listings, proceeds through data cleaning, exploratory data analysis (EDA), and feature engineering, and culminates in training a robust RandomForestRegressor model. The final model is deployed in a user-friendly web application built with Streamlit, which not only predicts car prices but also integrates with the Gemini API to deliver insightful, AI-generated summaries of the car's valuation.
✨ Features

    Accurate Price Prediction: Utilizes a RandomForest model to provide reliable price estimates.

    AI-Powered Analysis: Integrates Google's Gemini AI to explain the "why" behind a valuation.

    Interactive Web Interface: A clean and intuitive UI built with Streamlit for easy user interaction.

    Secure API Key Handling: Implements Streamlit's secrets management to keep API keys safe.

    Full Data Science Pipeline: Includes modular scripts for each step of the process, from cleaning to deployment.

🛠️ Technologies Used

    Programming Language: Python 3.9+

    Machine Learning: Scikit-learn

    Data Manipulation: Pandas

    Data Visualization: Matplotlib, Seaborn

    Web Framework: Streamlit

    AI Integration: Google Gemini API (via requests)

⚙️ Setup and Installation

Follow these steps to set up the project on your local machine.
1. Clone the Repository

git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME

2. Install Dependencies

It is recommended to create a virtual environment first.

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Then, install the required libraries:

pip install pandas scikit-learn seaborn matplotlib streamlit requests

3. Set Up Your Gemini API Key (Secure Method)

Your API key must be kept secret and should never be committed to GitHub.

    In the root folder of the project, create a new folder named .streamlit.

    Inside the .streamlit folder, create a new file named secrets.toml.

    Open secrets.toml and add your API key as follows:

    GEMINI_API_KEY = "YOUR_API_KEY_HERE"

The .gitignore file is already configured to ignore this file, ensuring it remains private.
🚀 Usage
1. Run the Data Pipeline

Before running the app for the first time, you need to process the data and train the model. Execute the scripts in order from your terminal:

python 01_data_loading.py
python 02_data_cleaning.py
python 03_eda_and_visualization.py
python 04_feature_engineering.py
python 05_model_training.py

This process will generate the car_price_model.pkl file, which the Streamlit app needs to function.
2. Launch the Web Application

Start the Streamlit app with the following command:

streamlit run 07_app.py

Your web browser will automatically open to the application's interface.
📁 Project Structure

.
├── 01_data_loading.py          # Loads the initial dataset
├── 02_data_cleaning.py         # Cleans data and handles missing values
├── 03_eda_and_visualization.py # Generates and saves exploratory plots
├── 04_feature_engineering.py   # Creates new features and encodes data
├── 05_model_training.py        # Trains and saves the ML model
├── 07_app.py                   # The main Streamlit application file
├── README.md                   # Project documentation
├── .gitignore                  # Specifies files for Git to ignore
└── (Your data file).csv        # The raw dataset

☁️ Deployment

This application is ready to be deployed on the Streamlit Community Cloud.

    Push your project (without the .streamlit folder) to a public GitHub repository.

    Sign in to share.streamlit.io.

    Click "New app" and connect your GitHub repository.

    Select the 07_app.py file.

    In the "Advanced settings," navigate to the "Secrets" tab.

    Paste the contents of your local .streamlit/secrets.toml file into the text area.

    Click "Deploy!".

📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
