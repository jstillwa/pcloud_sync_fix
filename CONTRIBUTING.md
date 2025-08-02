# Contributing to pCloud Sync Fixer

Thank you for your interest in contributing to pCloud Sync Fixer! This
document provides guidelines and information to help you contribute
effectively.

## How to Contribute

### Reporting Issues

If you encounter a bug or have a feature request, please open an issue on
GitHub with the following information:

- A clear and descriptive title
- A detailed description of the problem or enhancement
- Steps to reproduce the issue (if applicable)
- Your operating system and Python version
- Any relevant error messages or logs

### Code Contributions

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Ensure your code follows the existing style
5. Add or update tests as necessary
6. Submit a pull request with a clear description of your changes

## Development Setup

1. Clone your fork of the repository
2. Install dependencies using uv:

   ```bash
   uv sync
   ```

3. Make your changes
4. Test your changes thoroughly

## Code Style

- Follow PEP 8 guidelines for Python code
- Use clear, descriptive variable and function names
- Include docstrings for functions and classes
- Write comments to explain complex logic

## Testing

- Ensure all existing tests pass before submitting your pull request
- Add new tests for any functionality you introduce
- Test your changes with a real pCloud database if possible (make sure to
  backup first!)

## Pull Request Process

1. Ensure your pull request has a clear title and description
2. Link any related issues in your pull request description
3. Be responsive to feedback during the review process
4. Once approved, your pull request will be merged by a maintainer

## Community Guidelines

- Be respectful and inclusive in all interactions
- Provide constructive feedback on pull requests
- Follow the project's [Code of Conduct](CODE_OF_CONDUCT.md)

## About the pCloud Database

The [README](README.md) provides a comprehensive overview of the pCloud
database structure and how the pCloud client manages its sync state.

Thank you for helping improve pCloud Sync Fixer!
