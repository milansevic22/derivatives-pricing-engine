import numpy as np

from src.black_scholes import black_scholes_price
from src.monte_carlo import monte_carlo_european


def test_monte_carlo_close_to_black_scholes():
    """Test that Monte Carlo produces a price close to Black-Scholes."""

    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.20

    bs_price = black_scholes_price(
        S, K, T, r, 0.0, sigma, option_type="call"
    )

    mc_price = monte_carlo_european(
        S, K, T, r, sigma,
        M=500_000,
        option_type="call",
        seed=42,
    )

    assert np.isclose(mc_price, bs_price, atol=0.10)