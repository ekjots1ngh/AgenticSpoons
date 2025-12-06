/**
 * Monte Carlo Engine for Options Pricing
 * Uses variance reduction techniques
 */
#ifndef MONTE_CARLO_HPP
#define MONTE_CARLO_HPP

#include <vector>
#include <random>
#include <cmath>
#include <algorithm>

class MonteCarloEngine {
private:
    std::mt19937 rng;

public:
    MonteCarloEngine(unsigned seed = 42) : rng(seed) {}

    // Price European option with antithetic variates
    double price_european(double S0, double K, double T, double r, double sigma,
                         bool is_call, int n_paths = 100000) {
        std::normal_distribution<double> norm(0.0, 1.0);
        
        double drift = (r - 0.5 * sigma * sigma) * T;
        double diffusion = sigma * sqrt(T);
        double sum_payoffs = 0.0;

        // Antithetic variates for variance reduction
        for (int i = 0; i < n_paths / 2; ++i) {
            double z = norm(rng);
            
            // Positive path
            double ST1 = S0 * exp(drift + diffusion * z);
            double payoff1 = is_call ? std::max(0.0, ST1 - K) : std::max(0.0, K - ST1);
            
            // Antithetic path
            double ST2 = S0 * exp(drift - diffusion * z);
            double payoff2 = is_call ? std::max(0.0, ST2 - K) : std::max(0.0, K - ST2);
            
            sum_payoffs += (payoff1 + payoff2) / 2.0;
        }

        return exp(-r * T) * sum_payoffs / (n_paths / 2);
    }

    // Asian option pricing
    double price_asian(double S0, double K, double T, double r, double sigma,
                      bool is_call, int n_steps, int n_paths) {
        std::normal_distribution<double> norm(0.0, 1.0);
        
        double dt = T / n_steps;
        double drift = (r - 0.5 * sigma * sigma) * dt;
        double diffusion = sigma * sqrt(dt);
        double sum_payoffs = 0.0;

        for (int path = 0; path < n_paths; ++path) {
            double S = S0;
            double sum_S = 0.0;

            for (int step = 0; step < n_steps; ++step) {
                double z = norm(rng);
                S *= exp(drift + diffusion * z);
                sum_S += S;
            }

            double avg_price = sum_S / n_steps;
            double payoff = is_call ? std::max(0.0, avg_price - K) 
                                    : std::max(0.0, K - avg_price);
            sum_payoffs += payoff;
        }

        return exp(-r * T) * sum_payoffs / n_paths;
    }

    // Barrier option pricing
    double price_barrier(double S0, double K, double B, double T, double r, double sigma,
                        bool is_call, bool is_down_and_out, int n_steps, int n_paths) {
        std::normal_distribution<double> norm(0.0, 1.0);
        
        double dt = T / n_steps;
        double drift = (r - 0.5 * sigma * sigma) * dt;
        double diffusion = sigma * sqrt(dt);
        double sum_payoffs = 0.0;

        for (int path = 0; path < n_paths; ++path) {
            double S = S0;
            bool barrier_hit = false;

            for (int step = 0; step < n_steps; ++step) {
                double z = norm(rng);
                S *= exp(drift + diffusion * z);

                // Check barrier
                if (is_down_and_out && S <= B) {
                    barrier_hit = true;
                    break;
                } else if (!is_down_and_out && S >= B) {
                    barrier_hit = true;
                    break;
                }
            }

            if (!barrier_hit) {
                double payoff = is_call ? std::max(0.0, S - K) : std::max(0.0, K - S);
                sum_payoffs += payoff;
            }
        }

        return exp(-r * T) * sum_payoffs / n_paths;
    }

    // Simulate GBM paths
    std::vector<std::vector<double>> simulate_paths(
        double S0, double mu, double sigma, double T, int n_steps, int n_paths
    ) {
        std::normal_distribution<double> norm(0.0, 1.0);
        
        double dt = T / n_steps;
        double drift = (mu - 0.5 * sigma * sigma) * dt;
        double diffusion = sigma * sqrt(dt);

        std::vector<std::vector<double>> paths(n_paths, std::vector<double>(n_steps + 1));

        #pragma omp parallel for
        for (int path = 0; path < n_paths; ++path) {
            paths[path][0] = S0;
            double S = S0;

            for (int step = 1; step <= n_steps; ++step) {
                double z = norm(rng);
                S *= exp(drift + diffusion * z);
                paths[path][step] = S;
            }
        }

        return paths;
    }
};

#endif // MONTE_CARLO_HPP
