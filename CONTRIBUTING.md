# Contributing to Math Animation System

Thank you for considering contributing! This document will help you get started.

## 🌟 How Can I Contribute?

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating a new issue
3. **Include details:**
   - Your OS and Python/Node.js versions
   - The equation that caused the issue
   - Error messages and logs
   - Steps to reproduce

### Suggesting Features

1. **Check existing feature requests** first
2. **Describe your idea clearly:**
   - What problem does it solve?
   - How should it work?
   - Any examples or mockups?

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test your changes:** `python test_system.py`
5. **Commit with clear messages:** `git commit -m 'Add amazing feature'`
6. **Push to your fork:** `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## 🏗️ Development Setup

### 1. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/math-animator.git
cd math-animator
```

### 2. Set Up Environment

```bash
# Run setup script
./setup.sh

# Or manually:
npm install
pip install -r requirements.txt
```

### 3. Run Tests

```bash
python test_system.py
```

## 📝 Code Style

### Python

- Follow [PEP 8](https://pep8.org/)
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

Example:
```python
def process_equation(equation: str) -> dict:
    """
    Process a mathematical equation.
    
    Args:
        equation: The equation to process
        
    Returns:
        Dictionary with processing results
    """
    # Implementation here
    pass
```

### JavaScript

- Use consistent indentation (2 spaces)
- Add JSDoc comments for functions
- Handle errors gracefully

Example:
```javascript
/**
 * Process mathematical input
 * @param {string} input - The math expression
 * @returns {object} Processing results
 */
function processMathInput(input) {
    // Implementation here
}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python test_system.py

# Test specific component
python math_bridge.py

# Test with real equations
python main.py -f equations.txt --batch
```

### Adding Tests

When adding new features, please include tests:

```python
def test_new_feature():
    """Test the new feature"""
    # Your test code here
    assert result == expected
```

## 📚 Documentation

### Code Documentation

- Add docstrings to all public functions
- Update README.md for major features
- Add examples to QUICKSTART.md

### Commit Messages

Use clear, descriptive commit messages:

**Good:**
```
Add support for cubic equations
Fix LaTeX parsing for square roots
Improve animation timing configuration
```

**Not so good:**
```
Update stuff
Fix bug
Changes
```

### Pull Request Description

Include:
- **What** the PR does
- **Why** it's needed
- **How** it works
- **Testing** done
- **Screenshots/videos** if applicable

## 🎨 Animation Contributions

If you're improving animations:

1. **Test with multiple equations**
2. **Check different quality settings**
3. **Ensure smooth transitions**
4. **Consider timing and pacing**

## 🤝 Community Guidelines

- **Be respectful** and inclusive
- **Help others** when you can
- **Give constructive feedback**
- **Celebrate contributions** from everyone

## 📋 Checklist Before Submitting PR

- [ ] Code follows style guidelines
- [ ] Tests pass (`python test_system.py`)
- [ ] Added tests for new features
- [ ] Updated documentation
- [ ] Commit messages are clear
- [ ] PR description is complete

## 🏆 Recognition

Contributors will be:
- Listed in README.md
- Acknowledged in release notes
- Part of this growing community!

## 💬 Questions?

- Open a [Discussion](https://github.com/yourusername/math-animator/discussions)
- Join our community chat (if available)
- Email: your.email@example.com

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making Math Animation System better! 🙏
