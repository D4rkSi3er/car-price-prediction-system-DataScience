import streamlit as st
import pandas as pd
import pickle
from datetime import date
import os
import json
import requests

# Gemini API Integration
def get_gemini_analysis(car_details, predicted_price):
    """
    Gets a descriptive analysis of the car's valuation from the Gemini API.
    This function is now more robust to handle potential API errors.
    """
    api_key = "" 
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    prompt = f"""
    You are an expert car valuation assistant. Analyze the following car details and its predicted price. Provide a concise, helpful summary explaining the key factors influencing the valuation (e.g., age, mileage, ownership). End with a practical tip.

    Car Details:
    - Year: {car_details.get('year', 'N/A')}
    - Kms Driven: {car_details.get('kms_driven', 'N/A')}
    - Fuel: {car_details.get('fuel_type', 'N/A')}
    - Seller: {car_details.get('seller_type', 'N/A')}
    - Transmission: {car_details.get('transmission_type', 'N/A')}
    - Ownership: {car_details.get('owner_type', 'N/A')}
    Predicted Price: ₹{predicted_price:,.0f}
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    
    # error handling
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() 
        result = response.json()
        
        candidate = result.get('candidates', [])
        if not candidate:
            error_message = result.get('error', {}).get('message', 'No content generated.')
            st.warning(f"AI analysis could not be generated. Reason: {error_message}")
            return "Analysis failed. Please check your API key or the input details."

        content = candidate[0].get('content', {})
        parts = content.get('parts', [])
        if not parts:
            return "AI analysis returned empty content."

        return parts[0].get('text', "Analysis not available.")

    except requests.exceptions.RequestException as e:
        st.error(f"Network error connecting to Gemini API: {e}")
        return "AI analysis could not be generated due to a network issue."
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        st.error(f"Error parsing Gemini API response: {e}")
        return "AI analysis could not be generated due to an unexpected response format."


# load model
try:
    with open('car_price_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
    model = model_data['model']
    model_columns = model_data['columns']
except FileNotFoundError:
    st.error("Model file 'car_price_model.pkl' not found! Please run the training scripts first.")
    st.stop()

# Predicitons 
def predict_price(year, kms_driven, fuel_type, seller_type, transmission_type, owner_type):
    """
    Prepares user input and predicts car price.
    --- FIX: This function is rewritten to be robust against feature mismatch errors. ---
    """
    #input types
    input_df = pd.DataFrame(columns=model_columns)
    input_df.loc[0] = 0
    input_df['kms_driven'] = kms_driven
    input_df['car_age'] = date.today().year - year
    #fule type
    fuel_col = f"fuel_type_{fuel_type}"
    if fuel_col in input_df.columns:
        input_df[fuel_col] = 1
    # Seller Type 
    seller_col = f"seller_type_{seller_type}"
    if seller_col in input_df.columns:
        input_df[seller_col] = 1
        
    # Transmission Type
    trans_col = f"transmission_type_{transmission_type}"
    if trans_col in input_df.columns:
        input_df[trans_col] = 1
        
    # Owner Type
    owner_col = f"owner_type_{owner_type}"
    if owner_col in input_df.columns:
        input_df[owner_col] = 1
        
    input_df = input_df[model_columns]

    # Prediction
    prediction = model.predict(input_df)[0]
    return prediction

# UI with Streamlit
st.set_page_config(page_title="Car Price Predictor", layout="wide")
st.title("🚗 Car Price Prediction System with AI Insights")
st.markdown("Enter car details to get a predicted price and an expert analysis from Google's Gemini AI.")

with st.sidebar:
    st.header("Car Details")
    year = st.number_input("Manufacturing Year", 1990, date.today().year, 2015, help="Select the year the car was made.")
    kms = st.number_input("Kilometers Driven", 100, 500000, 70000, help="Enter the total kilometers the car has been driven.")
    fuel = st.selectbox("Fuel Type", ('Diesel', 'Petrol', 'CNG', 'LPG', 'Electric'))
    seller = st.selectbox("Seller Type", ('Individual', 'Dealer', 'Trustmark Dealer'))
    transmission = st.selectbox("Transmission Type", ('Manual', 'Automatic'))
    owner = st.selectbox("Ownership", ('First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car'))

if st.sidebar.button("Predict Price", use_container_width=True, type="primary"):
    predicted_price = predict_price(year, kms, fuel, seller, transmission, owner)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Prediction Result")
        st.metric(label="Predicted Selling Price", value=f"₹ {predicted_price:,.0f}")
    
    with col2:
        st.subheader("🤖 AI-Powered Analysis")
        with st.spinner('Generating...'):
            user_inputs_for_ai = {'year': year, 'kms_driven': kms, 'fuel_type': fuel, 'seller_type': seller, 'transmission_type': transmission, 'owner_type': owner}
            gemini_summary = get_gemini_analysis(user_inputs_for_ai, predicted_price)
            st.markdown(gemini_summary)
else:
    st.info("Please enter car details in the sidebar and click 'Predict Price'.")

