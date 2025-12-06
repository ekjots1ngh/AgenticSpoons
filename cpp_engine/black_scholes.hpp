/**
 * High-Performance Black-Scholes Engine in C++
 * 10-100x faster than Python for large-scale calculations
 */
#ifndef BLACK_SCHOLES_HPP
#define BLACK_SCHOLES_HPP

#include <cmath>
#include <vector>
#include <algorithm>

class BlackScholesEngine {
private:
    // Standard normal CDF (Abramowitz and Stegun approximation)
    static double norm_cdf(double x) {
        const double a1 =  0.254829592;
        const double a2 = -0.284496736;
        const double a3 =  1.421413741;
        const double a4 = -1.453152027;
        const double a5 =  1.061405429;
        const double p  =  0.3275911;

        int sign = (x < 0) ? -1 : 1;
        x = fabs(x) / sqrt(2.0);

        double t = 1.0 / (1.0 + p * x);
        double y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * exp(-x * x);

        return 0.5 * (1.0 + sign * y);
    }

    // Standard normal PDF
    static double norm_pdf(double x) {
        return (1.0 / sqrt(2.0 * M_PI)) * exp(-0.5 * x * x);
    }

    static double d1(double S, double K, double T, double r, double sigma) {
        return (log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T));
    }

    static double d2(double S, double K, double T, double r, double sigma) {
        return d1(S, K, T, r, sigma) - sigma * sqrt(T);
    }

public:
    // Call option price
    static double call_price(double S, double K, double T, double r, double sigma) {
        double d1_val = d1(S, K, T, r, sigma);
        double d2_val = d2(S, K, T, r, sigma);
        
        return S * norm_cdf(d1_val) - K * exp(-r * T) * norm_cdf(d2_val);
    }

    // Put option price
    static double put_price(double S, double K, double T, double r, double sigma) {
        double d1_val = d1(S, K, T, r, sigma);
        double d2_val = d2(S, K, T, r, sigma);
        
        return K * exp(-r * T) * norm_cdf(-d2_val) - S * norm_cdf(-d1_val);
    }

    // Delta
    static double delta(double S, double K, double T, double r, double sigma, bool is_call) {
        double d1_val = d1(S, K, T, r, sigma);
        return is_call ? norm_cdf(d1_val) : norm_cdf(d1_val) - 1.0;
    }

    // Gamma (same for call and put)
    static double gamma(double S, double K, double T, double r, double sigma) {
        double d1_val = d1(S, K, T, r, sigma);
        return norm_pdf(d1_val) / (S * sigma * sqrt(T));
    }

    // Vega (same for call and put)
    static double vega(double S, double K, double T, double r, double sigma) {
        double d1_val = d1(S, K, T, r, sigma);
        return S * norm_pdf(d1_val) * sqrt(T);
    }

    // Theta for call
    static double theta_call(double S, double K, double T, double r, double sigma) {
        double d1_val = d1(S, K, T, r, sigma);
        double d2_val = d2(S, K, T, r, sigma);
        
        double term1 = -(S * norm_pdf(d1_val) * sigma) / (2.0 * sqrt(T));
        double term2 = -r * K * exp(-r * T) * norm_cdf(d2_val);
        
        return (term1 + term2) / 365.0; // Daily theta
    }

    // Rho for call
    static double rho_call(double S, double K, double T, double r, double sigma) {
        double d2_val = d2(S, K, T, r, sigma);
        return K * T * exp(-r * T) * norm_cdf(d2_val) / 100.0;
    }

    // Implied volatility using Newton-Raphson
    static double implied_volatility(double option_price, double S, double K, double T, 
                                    double r, bool is_call, double initial_guess = 0.3) {
        double sigma = initial_guess;
        const int max_iterations = 100;
        const double tolerance = 1e-6;

        for (int i = 0; i < max_iterations; ++i) {
            double price = is_call ? call_price(S, K, T, r, sigma) 
                                   : put_price(S, K, T, r, sigma);
            double vega_val = vega(S, K, T, r, sigma);

            if (fabs(vega_val) < 1e-10) break;

            double diff = option_price - price;
            if (fabs(diff) < tolerance) return sigma;

            sigma += diff / vega_val;
            sigma = std::max(0.001, std::min(sigma, 5.0)); // Bounds
        }

        return sigma;
    }

    // Vectorized pricing for portfolio
    static std::vector<double> price_portfolio(
        const std::vector<double>& S_vec,
        const std::vector<double>& K_vec,
        const std::vector<double>& T_vec,
        const std::vector<double>& r_vec,
        const std::vector<double>& sigma_vec,
        const std::vector<bool>& is_call_vec
    ) {
        size_t n = S_vec.size();
        std::vector<double> prices(n);

        // OpenMP parallelization (if available)
        #pragma omp parallel for
        for (size_t i = 0; i < n; ++i) {
            prices[i] = is_call_vec[i] 
                ? call_price(S_vec[i], K_vec[i], T_vec[i], r_vec[i], sigma_vec[i])
                : put_price(S_vec[i], K_vec[i], T_vec[i], r_vec[i], sigma_vec[i]);
        }

        return prices;
    }
};

#endif // BLACK_SCHOLES_HPP
