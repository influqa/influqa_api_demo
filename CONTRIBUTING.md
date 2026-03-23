# Contributing to Influqa API Demo

Thank you for your interest in contributing to the Influqa API Demo repository! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [GitHub Issues](https://github.com/influqa/influqa_api_demo/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Screenshots if applicable

### Submitting Changes

1. **Fork the Repository**
   ```bash
   git clone https://github.com/influqa/influqa_api_demo.git
   cd influqa_api_demo
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

3. **Make Your Changes**
   - Follow the existing code style
   - Add/update documentation as needed
   - Test your changes

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

   Use conventional commit messages:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting)
   - `refactor:` - Code refactoring
   - `test:` - Test changes
   - `chore:` - Build/config changes

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## Code Style Guidelines

### JavaScript
- Use ES6+ syntax
- 2 spaces for indentation
- Single quotes for strings
- Semicolons required
- Max line length: 100 characters

### Python
- Follow PEP 8
- 4 spaces for indentation
- Use type hints where applicable
- Docstrings for functions and classes

### Shell Scripts
- Use `#!/bin/bash` shebang
- Quote all variables
- Use `shellcheck` for linting
- Add comments for complex operations

## Documentation

When adding new examples:

1. Include clear comments explaining the code
2. Add usage examples
3. Document all parameters
4. Include expected responses
5. Add error handling examples

## Testing

Before submitting:

- Test all code examples
- Verify API endpoints are correct
- Check for typos
- Ensure examples work with the latest API version

## Questions?

- Join our [Discord](https://discord.gg/influqa)
- Email: api-support@influqa.com

## Code of Conduct

Be respectful and constructive in all interactions. We aim to maintain a welcoming community for everyone.

Thank you for contributing! 🎉
