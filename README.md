# Derivatives Pricing and Volatility Analysis

## Overview

This project implements several core option pricing methods in Python and applies them to real SPY options data. I built it to develop a better understanding of how analytical, numerical and simulation-based pricing methods relate to each other, and how implied volatility can be extracted and analysed using market data.

The project includes Black-Scholes pricing and Greeks, a Newton-Raphson implied volatility solver, a Cox-Ross-Rubinstein binomial tree and Monte Carlo pricing. The implementations are tested against analytical results where possible.

I then use SPY options data from Databento to construct an implied volatility surface and examine how implied volatility varies across strike and maturity. A Black-Scholes implementation in C++ is also included as a small extension to compare the structure and performance of a compiled implementation.

## Features

- Black-Scholes pricing for European calls and puts with a continuous dividend yield
- Analytical Delta, Gamma, Vega, Theta and Rho
- Newton-Raphson implied volatility solver
- Cox-Ross-Rubinstein binomial tree for European and American options
- Monte Carlo pricing using simulated geometric Brownian motion
- Automated tests comparing numerical methods with analytical benchmarks
- SPY option chain processing using Databento market data
- Implied volatility smile, skew, term structure and surface analysis
- C++ implementation of Black-Scholes pricing with a simple performance benchmark

## Project Structure

```text
derivatives-pricing-engine/
├── src/
│   ├── __init__.py
│   ├── black_scholes.py
│   ├── implied_volatility.py
│   ├── binomial.py
│   └── monte_carlo.py
├── tests/
│   ├── test_black_scholes.py
│   ├── test_implied_volatility.py
│   ├── test_binomial.py
│   └── test_monte_carlo.py
├── notebooks/
│   ├── 01_black_scholes_exploration.ipynb
│   ├── 02_implied_volatility.ipynb
│   ├── 03_binomial_tree.ipynb
│   ├── 04_monte_carlo.ipynb
│   ├── 05_volatility_surface.ipynb
│   └── 06_volatility_analysis.ipynb
├── data/
│   └── spy_vol_surface_2026-09-15.csv
├── cpp/
│   └── black_scholes.cpp
├── pyproject.toml
└── README.md
```

## Pricing Models

### Black-Scholes

I implemented the Black-Scholes model for European call and put options, including a continuous dividend yield. The implementation also calculates Delta, Gamma, Vega, Theta and Rho.

The model provides the analytical benchmark used to check the numerical pricing methods elsewhere in the project.

### Implied Volatility

Implied volatility is calculated using the Newton-Raphson method. Starting from an initial volatility estimate, the algorithm repeatedly updates volatility using the difference between the model price and observed option price, with Vega used as the derivative.

The solver includes convergence checks and returns `NaN` when Vega becomes too small or the volatility estimate moves outside a reasonable range.

### Binomial Tree

The Cox-Ross-Rubinstein model is implemented using backward induction. It can price both European and American calls and puts.

For European options, increasing the number of time steps causes the binomial price to converge towards the Black-Scholes price. For American options, the value at each node is the maximum of the continuation value and the value from immediate exercise.

### Monte Carlo

European options are also priced using Monte Carlo simulation. Terminal asset prices are simulated under geometric Brownian motion and the discounted average payoff is used to estimate the option value.

I use the standard error of the simulated discounted payoffs to measure the statistical uncertainty in the Monte Carlo estimate.

## Model Validation

The pricing functions are separated into reusable modules in `src/` and tested using `pytest`.

The test suite currently contains six tests covering:

- Black-Scholes pricing against a known benchmark
- Dividend-adjusted put-call parity
- Recovery of a known volatility using the implied volatility solver
- Convergence of the European CRR model towards Black-Scholes
- The early exercise feature of an American put
- Monte Carlo pricing against the Black-Scholes benchmark using a fixed random seed

Running the full test suite gives:

```text
collected 6 items

tests/test_binomial.py ................. [ 33%]
tests/test_black_scholes.py ............ [ 66%]
tests/test_implied_volatility.py ....... [ 83%]
tests/test_monte_carlo.py .............. [100%]

6 passed
```

For the standard Black-Scholes example

```text
S = 100
K = 100
T = 1
r = 5%
q = 0%
sigma = 20%
```

the European call price is:

```text
10.45058357
```

This value is also reproduced by the C++ implementation.

## SPY Options Data

The market-data section uses an SPY options snapshot from 15 September 2026 obtained through Databento.

I first collect option definitions and quote data, then calculate bid-ask midpoints and apply filters to remove observations with stale quotes, large relative spreads or strikes far from the underlying price. Time to maturity is calculated for each contract before applying the implied volatility solver.

For the volatility calculations I use a flat risk-free rate of 3.64% and a continuous dividend yield approximation of 1%.

After the data cleaning and implied volatility calculations, I focus primarily on out-of-the-money options when examining the volatility surface.

The processed dataset used for the analysis is included in:

```text
data/spy_vol_surface_2026-09-15.csv
```

## Implied Volatility Analysis

The SPY snapshot shows a clear negative relationship between moneyness and implied volatility around the at-the-money region. Lower-strike options trade at higher implied volatilities than comparable higher-strike options.

To quantify this, I estimate a simple linear relationship between implied volatility and moneyness for options between 0.95 and 1.05 moneyness.

The estimated slopes are:

| Expiration | IV slope | R-squared |
|---|---:|---:|
| 18 Sep 2026 | -2.684 | 0.971 |
| 16 Oct 2026 | -0.971 | 0.975 |
| 20 Nov 2026 | -0.674 | 0.997 |
| 18 Dec 2026 | -0.567 | 0.994 |
| 19 Mar 2027 | -0.269 | 0.770 |

The negative slope is present across all five maturities in the sample, but its magnitude generally decreases with maturity. The shortest-dated options therefore display a much steeper local skew than the longer-dated contracts.

Another way of looking at the skew is to compare implied volatility around 95% and 105% moneyness. Excluding the very short September maturity, the difference is approximately:

| Expiration | 95% vs 105% IV difference |
|---|---:|
| 16 Oct 2026 | 8.74 vol points |
| 20 Nov 2026 | 6.29 vol points |
| 18 Dec 2026 | 5.51 vol points |
| 19 Mar 2027 | 3.81 vol points |

This gives another indication that the downside volatility premium in this snapshot becomes less pronounced at longer maturities.

## ATM Term Structure

I also examine the median implied volatility of options close to at-the-money, using moneyness between 0.99 and 1.01.

| Expiration | Median ATM IV |
|---|---:|
| 18 Sep 2026 | 16.28% |
| 16 Oct 2026 | 13.60% |
| 20 Nov 2026 | 15.10% |
| 18 Dec 2026 | 15.34% |
| 19 Mar 2027 | 16.18% |

The term structure is not monotonic in this snapshot. Implied volatility falls from the shortest maturity into October before increasing again across the later expirations.

Taken together, the strike and maturity analysis shows that the volatility surface contains structure in both dimensions rather than being well represented by a single constant volatility parameter.

## C++ Implementation

As an extension to the Python project, I reimplemented the Black-Scholes pricing function in C++.

The C++ implementation uses the same model inputs and reproduces the Python Black-Scholes benchmark:

```text
Call price: 10.45058357
Put price:   5.57352602
```

I also ran a simple benchmark of one million call price calculations using the compiled implementation.

On my machine, the benchmark produced:

```text
Priced 1000000 options in 60.3341 ms
Average time per price: 0.0603 microseconds
```

This benchmark is intended as an indication of the performance of the compiled implementation on my machine rather than a controlled comparison between Python and C++. A direct speed comparison would depend on implementation choices such as scalar Python, NumPy vectorisation and compiler optimisation.

## Limitations

There are several limitations to the market-data analysis.

SPY options are American-style, while the implied volatility calculations use a European Black-Scholes model. SPY also pays discrete dividends, whereas I approximate dividends using a constant continuous dividend yield.

The risk-free rate and dividend yield are held constant rather than being estimated separately for each maturity.

Short-dated implied volatility is particularly sensitive to small changes in option prices and time to maturity. This contributes to greater instability in the shortest maturity.

The analysis is also based on a single market snapshot. The results describe the shape of the SPY volatility surface at that point in time and should not be interpreted as a persistent relationship across different market regimes.

These simplifications were kept deliberately so that the project remained focused on implementing and understanding the pricing methods and volatility calculations.

## Running the Tests

From the project root:

```bash
pytest
```

The current test suite should return:

```text
6 passed
```

## C++ Compilation

The C++ implementation was compiled on Windows using the Microsoft Visual C++ compiler.

From a Visual Studio developer environment:

```cmd
cl /EHsc /O2 cpp\black_scholes.cpp /Fe:cpp\black_scholes.exe
```

The executable can then be run with:

```cmd
cpp\black_scholes.exe
```

## Tools and Libraries

The project primarily uses:

- Python
- NumPy
- pandas
- SciPy
- Matplotlib
- pytest
- Databento
- C++

## AI Use Disclosure

I used AI tools during this project as a learning and development aid. This included discussing quantitative finance concepts, debugging code, improving code structure and documentation, and reviewing implementation choices.

The project was developed interactively rather than generated as a complete solution. I worked through the pricing methods, numerical techniques, data processing and volatility analysis myself, tested the implementations, and reviewed the code and results throughout. I am responsible for the final methodology, implementation, analysis and conclusions presented in this repository.