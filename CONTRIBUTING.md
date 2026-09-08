# Contributing to ByteBreaker

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black mypy

# Run tests
pytest

# Check formatting
black .

# Type checking
mypy .
Code Style

    Follow PEP 8

    Use type hints

    Write docstrings

    Add tests for new features

    Keep functions small and focused

Commit Messages

Use conventional commits:

    feat: Add new feature

    fix: Fix bug

    docs: Update documentation

    test: Add tests

    refactor: Refactor code

Pull Request Process

    Update documentation

    Add tests

    Ensure all tests pass

    Update CHANGELOG.md

    Get code review

    Merge

Security

    Never commit credentials

    Always validate input

    Use authorization checks

    Follow security best practices

    Report vulnerabilities responsibly

Testing

    Write unit tests for new code

    Ensure coverage stays above 80%

    Test edge cases

    Test error handling

    Test security features

Documentation

    Update README.md

    Update API docs

    Add examples

    Document breaking changes

    Keep changelog updated

Questions?

Open an issue or contact the maintainers.
