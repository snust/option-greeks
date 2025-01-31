import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from options_calculator import calculate_greeks
import plotly.graph_objects as go

def main():
    st.title("Options greeks dashboard")
    
    # Input parameters section
    st.header("Input parameters")
    
    # Create two columns for inputs
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        long_short = st.selectbox("Long / Short", ["Long", "Short"])
        current_price = st.number_input("Current Stock Price", value=100.0, min_value=0.01)
        days_to_expiry = st.number_input("Days to Expiry", value=30, min_value=1)
        risk_free_rate = st.number_input("Risk-free Rate (%)", value=1.5, min_value=0.1)
    
    with input_col2:
        option_type = st.selectbox("Option Type", ["Call", "Put"])
        strike_price = st.number_input("Strike Price", value=current_price, min_value=0.01)
        volatility = st.number_input("Implied Volatility (%)", value=30.0, min_value=0.01)
    
    # Calculate greeks
    greeks = calculate_greeks(
        current_price,
        strike_price,
        days_to_expiry / 365,  # Convert days to years
        risk_free_rate / 100,
        volatility / 100,
        option_type.lower(),
        long_short.lower()
    )
    
    # Option Greeks section
    st.header("Option greeks")

    # Create dataframe with greeks and price
    greeks_df = pd.DataFrame({
        'Metric': ['Delta', 'Gamma', 'Theta', 'Vega', 'Theoretical Price'],
        'Value': [
            f"{greeks['delta']:.4f}",
            f"{greeks['gamma']:.4f}", 
            f"{greeks['theta']:.4f}",
            f"{greeks['vega']:.4f}",
            f"${greeks['price']:.2f}"
        ]
    })

    # Display dataframe
    st.dataframe(greeks_df, hide_index=True)

    # Create data for line plots
    days_range = np.linspace(1, days_to_expiry + 20, 10)
    vol_range = np.linspace(0.01, 2.0, 50)
    
    # Create dataframes for plotting
    # Days to Expiry analysis (keeping current volatility)
    days_data = {
        'Days to Expiry': days_range,
        'Theta': []
    }
    
    for days in days_range:
        result = calculate_greeks(
            current_price,
            strike_price,
            days / 365,
            risk_free_rate / 100,
            volatility / 100,
            option_type.lower(),
            long_short.lower()
        )
        days_data['Theta'].append(result['theta'])

    days_df = pd.DataFrame(days_data)

    # Display line charts
    st.header("Greeks Analysis")
    
    # Days to Expiry Analysis
    st.subheader("Theta changes over time")
    st.line_chart(days_df.set_index('Days to Expiry'))
    
    # Volatility analysis (keeping current days to expiry)
    vol_data = {
        'Volatility (%)': vol_range * 100,
        'Delta': [],
        'Gamma': [],
        'Theta': [],
        'Vega': []
    }
    
    for vol in vol_range:
        result = calculate_greeks(
            current_price,
            strike_price,
            days_to_expiry/365,
            risk_free_rate / 100,
            vol / 100,
            option_type.lower(),
            long_short.lower()
        )
        vol_data['Delta'].append(result['delta'])
        vol_data['Gamma'].append(result['gamma'])
        vol_data['Theta'].append(result['theta'])
        vol_data['Vega'].append(result['vega'])
    
    vol_df = pd.DataFrame(vol_data)

    
    
    # Volatility Analysis
    st.subheader("Greeks vs Implied Volatility")
    st.line_chart(vol_df.set_index('Volatility (%)'))

if __name__ == "__main__":
    main()