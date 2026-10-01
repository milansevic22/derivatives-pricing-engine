import numpy as np

from src.black_scholes import black_scholes_price



def test_black_scholes_known_value():
    """Test Black-Scholes against a known benchmark price."""

    call = black_scholes_price(
        S=100,
        K=100,
        T=1,
        r=0.05,
        q=0.0,
        sigma=0.20,
        option_type="call",
    )

    expected_price = 10.45058357

    assert np.isclose(call, expected_price, atol=1e-6)


def test_put_call_parity():
    """Test dividend-adjusted put-call parity."""

    S = 100
    K = 100
    T = 1
    r = 0.05
    q = 0.02
    sigma = 0.20

    call = black_scholes_price(
        S, K, T, r, q, sigma, option_type="call"
    )

    put = black_scholes_price(
        S, K, T, r, q, sigma, option_type="put"
    )

    left_side = call - put

    right_side = (
        S * np.exp(-q * T)
        - K * np.exp(-r * T)
    )

    assert np.isclose(left_side, right_side, atol=1e-10)