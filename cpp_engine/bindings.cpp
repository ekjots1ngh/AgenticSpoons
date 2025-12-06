/**
 * Python bindings for C++ engines
 */
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "black_scholes.hpp"
#include "monte_carlo.hpp"

namespace py = pybind11;

PYBIND11_MODULE(cpp_quant_engine, m) {
    m.doc() = "High-performance quantitative finance engine in C++";

    py::class_<BlackScholesEngine>(m, "BlackScholesEngine")
        .def_static("call_price", &BlackScholesEngine::call_price,
                   py::arg("S"), py::arg("K"), py::arg("T"), py::arg("r"), py::arg("sigma"))
        .def_static("put_price", &BlackScholesEngine::put_price)
        .def_static("delta", &BlackScholesEngine::delta)
        .def_static("gamma", &BlackScholesEngine::gamma)
        .def_static("vega", &BlackScholesEngine::vega)
        .def_static("theta_call", &BlackScholesEngine::theta_call)
        .def_static("rho_call", &BlackScholesEngine::rho_call)
        .def_static("implied_volatility", &BlackScholesEngine::implied_volatility)
        .def_static("price_portfolio", &BlackScholesEngine::price_portfolio);

    py::class_<MonteCarloEngine>(m, "MonteCarloEngine")
        .def(py::init<unsigned>(), py::arg("seed") = 42)
        .def("price_european", &MonteCarloEngine::price_european)
        .def("price_asian", &MonteCarloEngine::price_asian)
        .def("price_barrier", &MonteCarloEngine::price_barrier)
        .def("simulate_paths", &MonteCarloEngine::simulate_paths);
}
