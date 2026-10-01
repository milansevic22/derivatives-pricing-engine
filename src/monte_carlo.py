import numpy as np


def monte_carlo_european(
    S0, K, T, r, sigma, M, option_type="call", seed=None
):
    """
    Price a European call or put option using Monte Carlo simulation
    under geometric Brownian motion.

    Parameters
    ----------
    S0 : float
        Current underlying price.
    K : float
        Strike price.
    T : float
        Time to maturity in years.
    r : float
        Continuously compounded risk-free rate.
    sigma : float
        Annualised volatility.
    M : int
        Number of simulated terminal prices.
    option_type : str
        Either "call" or "put".
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    float
        Estimated option price.
    """

    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(M)

    drift = (r - 0.5 * sigma**2) * T
    diffusion = sigma * np.sqrt(T) * Z

    ST = S0 * np.exp(drift + diffusion)

    if option_type == "call":
        payoff = np.maximum(ST - K, 0)

    elif option_type == "put":
        payoff = np.maximum(K - ST, 0)

    else:
        raise ValueError("option_type must be either a 'call' or 'put'")

    option_price = np.exp(-r * T) * np.mean(payoff)

    return option_price