#!/bin/bash

echo "Generating status badges..."

# This script appends badges to README.md if they don't already exist
if ! grep -q "CI/CD" README.md; then
    cat >> README.md << 'BADGES'

## Status & Badges

[![CI/CD](https://github.com/yourusername/agentspoons/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/yourusername/agentspoons/actions)
[![codecov](https://codecov.io/gh/yourusername/agentspoons/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/agentspoons)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

BADGES
    echo "✅ Badges added to README.md"
else
    echo "✅ Badges already present in README.md"
fi
