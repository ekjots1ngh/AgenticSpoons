
from setuptools import setup, find_packages

setup(
    name="agentspoons-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests", "websockets"],
    author="Ekjot Singh",
    description="Official SDK for AgentSpoons Volatility Oracle",
    url="https://github.com/yourusername/agentspoons",
)
