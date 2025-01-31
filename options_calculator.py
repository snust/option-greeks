import numpy as np
from scipy.stats import norm

def calculate_greeks(S, K, T, r, sigma, option_type, position='long'):
    """
    Calculate option greeks using Black-Scholes formulas
    
    Parameters:
    S: Current stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free rate
    sigma: Volatility
    option_type: 'call' or 'put'
    position: 'long' or 'short' (default: 'long')
    
    Returns:
    Dictionary containing the option price and greeks
    """
    try:
        # Calculate d1 and d2
        d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        
        # Calculate components used in multiple formulas
        Nd1 = norm.cdf(d1)
        Nd2 = norm.cdf(d2)
        npd1 = norm.pdf(d1)
        
        if option_type == 'call':
            # Call option calculations
            price = S*Nd1 - K*np.exp(-r*T)*Nd2
            delta = Nd1
            theta = (-S*sigma*npd1/(2*np.sqrt(T)) - 
                    r*K*np.exp(-r*T)*Nd2)/365
            rho = K*T*np.exp(-r*T)*Nd2/100  # Divided by 100 to match market convention
        else:
            # Put option calculations
            Nnd1 = norm.cdf(-d1)
            Nnd2 = norm.cdf(-d2)
            price = K*np.exp(-r*T)*Nnd2 - S*Nnd1
            delta = Nd1 - 1
            theta = (-S*sigma*npd1/(2*np.sqrt(T)) + 
                    r*K*np.exp(-r*T)*Nnd2)/365
            rho = -K*T*np.exp(-r*T)*Nnd2/100  # Divided by 100 to match market convention
        
        # Greeks that are same for calls and puts
        gamma = npd1/(S*sigma*np.sqrt(T))
        vega = S*np.sqrt(T)*npd1/100  # Divided by 100 to match market convention
        
        # Adjust signs based on position
        multiplier = -1 if position == 'short' else 1
        price *= multiplier
        delta *= multiplier
        gamma *= multiplier
        theta *= multiplier
        vega *= multiplier
        rho *= multiplier
        
        greeks = {
            'price': price,
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'rho': rho
        }
        
        return greeks
        
    except Exception as e:
        print(f"Error calculating greeks: {e}")
        return {
            'price': 0,
            'delta': 0,
            'gamma': 0,
            'theta': 0,
            'vega': 0,
            'rho': 0
        }