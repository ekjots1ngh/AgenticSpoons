from setuptools import setup, Extension
import pybind11
import sys

# Compiler-specific flags
extra_compile_args = ['-std=c++17', '-O3']
extra_link_args = []

if sys.platform == 'win32':
    # Windows (MSVC)
    extra_compile_args = ['/std:c++17', '/O2', '/openmp']
    extra_link_args = []
else:
    # Linux/Mac (GCC/Clang)
    extra_compile_args = ['-std=c++17', '-O3', '-fopenmp']
    extra_link_args = ['-fopenmp']

ext_modules = [
    Extension(
        'cpp_quant_engine',
        ['bindings.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args
    ),
]

setup(
    name='cpp_quant_engine',
    version='1.0.0',
    description='High-performance quantitative finance engine',
    ext_modules=ext_modules,
    zip_safe=False,
)
