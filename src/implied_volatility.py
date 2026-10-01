import numpy as np
from scipy.stats import norm

from .black_scholes import black_scholes_price

def Newton_Raphson_iv(S, K, T, r, q, market_price, option_type="call"):

    """
    Estimate implied volatility using the Newton-Raphson method.

    Returns np.nan if the algorithm fails to converge or encounters
    an invalid volatility update.
    """

    sigma = 0.20
    tolerance = 1e-6
    
    for x in range(100):
        
        model_price = black_scholes_price(S,K,T,r,q,sigma,option_type)
        
        error = model_price - market_price

       

        if abs(error) < tolerance:
            return sigma


        d1 = (np.log(S/K) + (r - q + 0.5 * sigma**2)* T) / (sigma * np.sqrt(T))

        

        vega = (S*np.exp(-q*T) * norm.pdf(d1) * np.sqrt(T))

        if abs(vega) < 1e-8:
            return np.nan

        sigma_new = sigma - error / vega

        if sigma_new <= 0 or sigma_new > 5:
            return np.nan

        sigma = sigma_new


    return np.nan


