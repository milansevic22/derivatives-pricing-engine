#include <chrono>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>


double normal_cdf(double x)
{
    return 0.5 * std::erfc(-x / std::sqrt(2.0));
}


double black_scholes_price(
    double S,
    double K,
    double T,
    double r,
    double q,
    double sigma,
    const std::string& option_type)
{
    double d1 = (
        std::log(S / K)
        + (r - q + 0.5 * sigma * sigma) * T
    ) / (sigma * std::sqrt(T));

    double d2 = d1 - sigma * std::sqrt(T);

    if (option_type == "call")
    {
        return (
            S * std::exp(-q * T) * normal_cdf(d1)
            - K * std::exp(-r * T) * normal_cdf(d2)
        );
    }

    if (option_type == "put")
    {
        return (
            K * std::exp(-r * T) * normal_cdf(-d2)
            - S * std::exp(-q * T) * normal_cdf(-d1)
        );
    }

    throw std::invalid_argument("option_type must be 'call' or 'put'");
}


int main()
{
    double S = 100.0;
    double K = 100.0;
    double T = 1.0;
    double r = 0.05;
    double q = 0.0;
    double sigma = 0.20;

    double call_price = black_scholes_price(
        S, K, T, r, q, sigma, "call"
    );

    double put_price = black_scholes_price(
        S, K, T, r, q, sigma, "put"
    );

    std::cout << std::fixed << std::setprecision(8);

    std::cout << "Call price: " << call_price << '\n';
    std::cout << "Put price:  " << put_price << '\n';

    const int iterations = 1'000'000;
    double total = 0.0;

    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < iterations; ++i)
    {
        total += black_scholes_price(
            S, K, T, r, q, sigma, "call"
        );
    }

    auto end = std::chrono::high_resolution_clock::now();

    double elapsed_ms =
        std::chrono::duration<double, std::milli>(end - start).count();

    std::cout << "\nPriced " << iterations
              << " options in " << elapsed_ms << " ms\n";

    std::cout << "Average time per price: "
              << (elapsed_ms * 1000.0 / iterations)
              << " microseconds\n";

    std::cout << "Checksum: " << total << '\n';

    return 0;
}