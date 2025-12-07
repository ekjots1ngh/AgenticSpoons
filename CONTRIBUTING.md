# Contributing to AgentSpoons

Thank you for your interest in contributing. AgentSpoons is an open-source project and we welcome community involvement.

## Ways to Contribute

- Report bugs
- Suggest features
- Improve documentation
- Submit pull requests
- Star the repository
- Share the project

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/agentspoons.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Make changes
5. Test: `pytest tests/ -v`
6. Commit: `git commit -m "Add feature"`
7. Push: `git push origin feature/your-feature`
8. Open a pull request

## Development Setup
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v --cov=src

# Lint code
flake8 src/
black src/

# Type checking
mypy src/
```

## Pull Request Checklist

- [ ] Tests pass (`pytest`)
- [ ] Code is formatted (`black`)
- [ ] No linting errors (`flake8`)
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Pull request description explains changes

## Bug Reports

Use the issue template and include:
- Description of the bug
- Steps to reproduce
- Expected versus actual behaviour
- Environment details
- Screenshots (if applicable)

## Community

- Discord: [Join here](https://discord.gg/agentspoons)
- Twitter: [@agentspoons](https://twitter.com/agentspoons)
- Email: ekjot@agentspoons.io

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
