import numpy as np
from scipy.stats import norm


def black_scholes_price(S, K, T, r, q, sigma, option_type="call"):
    """
    Price a European call or put option using the Black-Scholes model
    with a continuous dividend yield.

    Parameters
    ----------
    S : float
        Current underlying price.
    K : float
        Strike price.
    T : float
        Time to maturity in years.
    r : float
        Continuously compounded risk-free rate.
    q : float
        Continuous dividend yield.
    sigma : float
        Annualised volatility.
    option_type : str
        Either "call" or "put".

    Returns
    -------
    float
        Black-Scholes option price.
    """

    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = (S * np.exp(-q * T) * norm.cdf(d1)- K * np.exp(-r * T) * norm.cdf(d2))

    elif option_type == "put":
        price = (K * np.exp(-r * T) * norm.cdf(-d2)- S * np.exp(-q * T) * norm.cdf(-d1))

    else:
        raise ValueError("option_type must be either a 'call' or a 'put'")

    return price




def black_scholes_greeks(S, K, T, r, q, sigma, option_type="call"):
    """
    Calculate Black-Scholes Greeks for a European call or put
    with a continuous dividend yield.

    Returns delta, gamma, vega, theta and rho.

    Vega and rho are reported per 1 percentage-point change.
    Theta is reported per calendar day.
    """

    d1 = (
        np.log(S / K) + (r - q + 0.5 * sigma**2) * T
    ) / (sigma * np.sqrt(T))

    d2 = d1 - sigma * np.sqrt(T)

    if option_type not in ("call", "put"):
        raise ValueError("option_type must be either 'call' or 'put'")

    if option_type == "call":
        delta = np.exp(-q * T) * norm.cdf(d1)
    else:
        delta = np.exp(-q * T) * (norm.cdf(d1) - 1)

    gamma = (
        np.exp(-q * T) * norm.pdf(d1)
        / (S * sigma * np.sqrt(T))
    )

    vega = (
        S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)
    ) / 100

    if option_type == "call":
        theta = (
            -S * np.exp(-q * T) * norm.pdf(d1) * sigma
            / (2 * np.sqrt(T))
            - r * K * np.exp(-r * T) * norm.cdf(d2)
            + q * S * np.exp(-q * T) * norm.cdf(d1)
        ) / 365

        rho = (
            K * T * np.exp(-r * T) * norm.cdf(d2)
        ) / 100

    else:
        theta = (
            -S * np.exp(-q * T) * norm.pdf(d1) * sigma
            / (2 * np.sqrt(T))
            + r * K * np.exp(-r * T) * norm.cdf(-d2)
            - q * S * np.exp(-q * T) * norm.cdf(-d1)
        ) / 365

        rho = (
            -K * T * np.exp(-r * T) * norm.cdf(-d2)
        ) / 100

    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
    }