import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from options_calculator import calculate_greeks

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

    # Display line charts
    st.header("Greeks Analysis")

    # Create two columns for inputs
    input_col3, input_col4 = st.columns(2)

    with input_col3:
        greek = st.selectbox("Greek", ["Delta", "Gamma", "Theta", "Vega", "Rho"])

    with input_col4:
        changes = st.selectbox("Time / Implied Volatility", ["Time", "Implied Volatility"])
    
    # Days to Expiry Analysis
    st.subheader(greek + " against " + changes)
    # Generate price range around strike price (±50%)
    price_range = np.linspace(strike_price * 0.5, strike_price * 1.5, 100)
    
    # Initialize dataframe to store values
    df = pd.DataFrame()
    df['Price'] = price_range
    
    if changes == "Time":
        # Calculate for different time periods
        time_periods = [(days_to_expiry/4)/365, (days_to_expiry/2)/365, days_to_expiry/365]
        labels = [f"{days_to_expiry//4} days", f"{days_to_expiry//2} days", f"{days_to_expiry} days"]
        
        for i, t in enumerate(time_periods):
            values = []
            for price in price_range:
                result = calculate_greeks(
                    price,
                    strike_price,
                    t,
                    risk_free_rate / 100,
                    volatility / 100,
                    option_type.lower(),
                    long_short.lower()
                )
                values.append(result[greek.lower()])
            df[labels[i]] = values
            
    else:  # Implied Volatility analysis
        # Calculate for different volatilities
        vol_levels = [(volatility*0.5)/100, volatility/100, (volatility*1.5)/100]
        labels = [f"{volatility*0.5}% IV", f"{volatility}% IV", f"{volatility*1.5}% IV"]
        
        for i, vol in enumerate(vol_levels):
            values = []
            for price in price_range:
                result = calculate_greeks(
                    price,
                    strike_price,
                    days_to_expiry / 365,
                    risk_free_rate / 100,
                    vol,
                    option_type.lower(),
                    long_short.lower()
                )
                values.append(result[greek.lower()])
            df[labels[i]] = values

    # Set price as index for the line chart
    df = df.set_index('Price')
    
    # Display the line chart using streamlit
    st.line_chart(df)
    
    # Add note about strike price
    st.caption(f"Strike price: ${strike_price:.2f}")

if __name__ == "__main__":
    main()