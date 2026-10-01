import numpy as np

from src.black_scholes import black_scholes_price
from src.binomial import crr_price


def test_crr_converges_to_black_scholes():
    """Test that a European CRR price converges toward Black-Scholes."""

    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.20

    bs_price = black_scholes_price(
        S, K, T, r, 0.0, sigma, option_type="call"
    )

    crr_value = crr_price(
        S, K, T, r, sigma, N=500,
        option_type="call",
        american=False,
    )

    assert np.isclose(crr_value, bs_price, atol=0.01)


def test_american_put_at_least_european_put():
    """Test that the American put is worth at least the European put."""

    european_put = crr_price(
        100, 100, 1, 0.05, 0.20, N=500,
        option_type="put",
        american=False,
    )

    american_put = crr_price(
        100, 100, 1, 0.05, 0.20, N=500,
        option_type="put",
        american=True,
    )

    assert american_put >= european_put