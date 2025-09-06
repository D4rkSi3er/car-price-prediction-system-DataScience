import streamlit as st
import pandas as pd
import pickle
from datetime import date
import json
import requests

# AI
def get_gemini_analysis(car_details, predicted_price):
    """
    Gets a descriptive analysis of the car's valuation from the Gemini API.
    Reads the API key securely from Streamlit's secrets manager.
    """
    try:
        # API key
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error("Gemini API key not found. Please add it to your secrets file.")
        return "API key not configured. Cannot generate AI analysis."

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    prompt = f"""
    You are an expert car valuation assistant. Analyze the following car details and its predicted price. Provide a concise, helpful summary in plain language. Explain the key factors influencing the valuation (e.g., age, mileage, ownership). End with a practical tip for a potential buyer or seller.

    Car Details:
    - Manufacturing Year: {car_details.get('year', 'N/A')}
    - Kilometers Driven: {car_details.get('kms_driven', 'N/A')} km
    - Fuel Type: {car_details.get('fuel_type', 'N/A')}
    - Seller Type: {car_details.get('seller_type', 'N/A')}
    - Transmission: {car_details.get('transmission_type', 'N/A')}
    - Ownership: {car_details.get('owner_type', 'N/A')}
    
    Predicted Selling Price: ₹{predicted_price:,.0f}
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        
        candidate = result.get('candidates', [{}])[0]
        content = candidate.get('content', {}).get('parts', [{}])[0]
        return content.get('text', "Analysis not available.")

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
    st.error("Model file 'car_price_model.pkl' not found! Please run the training pipeline first (scripts 01-05).")
    st.stop()

def predict_price(year, kms_driven, fuel_type, seller_type, transmission_type, owner_type):
    input_df = pd.DataFrame(columns=model_columns)
    input_df.loc[0] = 0  
    input_df['kms_driven'] = kms_driven
    input_df['car_age'] = date.today().year - year
    
    # encoding
    if f"fuel_type_{fuel_type}" in input_df.columns: input_df[f"fuel_type_{fuel_type}"] = 1
    if f"seller_type_{seller_type}" in input_df.columns: input_df[f"seller_type_{seller_type}"] = 1
    if f"transmission_type_{transmission_type}" in input_df.columns: input_df[f"transmission_type_{transmission_type}"] = 1
    if f"owner_type_{owner_type}" in input_df.columns: input_df[f"owner_type_{owner_type}"] = 1
    
    # reorder
    input_df = input_df[model_columns]
    prediction = model.predict(input_df)[0]
    return prediction
# UI
st.set_page_config(page_title="Car Price Predictor", layout="wide", initial_sidebar_state="expanded")
st.title("🚗 Car Price Prediction System with AI Insights")
st.markdown("Enter car details to get a predicted price and an expert analysis from Google's Gemini AI.")

with st.sidebar:
    st.header("Input Car Details")
    year = st.number_input("Manufacturing Year", 1990, date.today().year, 2015)
    kms = st.number_input("Kilometers Driven", 100, 500000, 70000)
    fuel = st.selectbox("Fuel Type", ('Diesel', 'Petrol', 'CNG', 'LPG', 'Electric'))
    seller = st.selectbox("Seller Type", ('Individual', 'Dealer', 'Trustmark Dealer'))
    transmission = st.selectbox("Transmission Type", ('Manual', 'Automatic'))
    owner = st.selectbox("Ownership", ('First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car'))

if st.sidebar.button("Predict Price", use_container_width=True, type="primary"):
    predicted_price = predict_price(year, kms, fuel, seller, transmission, owner)
    
    st.header("Prediction Result")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric(label="Predicted Selling Price (INR)", value=f"₹ {predicted_price:,.0f}")
    
    with col2:
        with st.spinner('🤖 Generating AI Analysis...'):
            user_inputs = {'year': year, 'kms_driven': kms, 'fuel_type': fuel, 'seller_type': seller, 'transmission_type': transmission, 'owner_type': owner}
            gemini_summary = get_gemini_analysis(user_inputs, predicted_price)
            st.info(gemini_summary)
else:
    st.info("Please enter car details in the sidebar and click 'Predict Price' to see the valuation.")

