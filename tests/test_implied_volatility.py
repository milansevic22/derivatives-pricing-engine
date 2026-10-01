import numpy as np

from src.black_scholes import black_scholes_price
from src.implied_volatility import Newton_Raphson_iv


def test_implied_volatility_recovery():
    """Test that the IV solver recovers a known volatility."""

    S = 100
    K = 100
    T = 1
    r = 0.05
    q = 0.02
    true_sigma = 0.25

    market_price = black_scholes_price(
        S, K, T, r, q, true_sigma, option_type="call"
    )

    estimated_sigma = Newton_Raphson_iv(
        S, K, T, r, q, market_price, option_type="call"
    )

    assert np.isclose(estimated_sigma, true_sigma, atol=1e-6)