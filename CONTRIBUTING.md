# Contributing to Death Counter

Thank you for your interest in contributing to Death Counter! 🎮

## 🤝 How to Contribute

### 1. Fork & Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/DeathCounter-py.git
cd DeathCounter-py
```

### 2. Set up Development Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 4. Make Your Changes
- Follow the existing code style
- Add comments for complex logic
- Test your changes thoroughly

### 5. Commit & Push
```bash
git add .
git commit -m "feat: add support for new game"
git push origin feature/your-feature-name
```

### 6. Create Pull Request
Open a PR on GitHub with a clear description of your changes.

## 🐛 Bug Reports

When reporting bugs, please include:

- **OS**: Windows/Linux/macOS version
- **Python version**: `python --version`
- **Game**: Which FromSoftware game you're monitoring
- **Error message**: Full error traceback if available
- **Screenshots**: If GUI-related
- **Steps to reproduce**: Detailed steps

### Bug Report Template
```markdown
**Bug Description**
A clear description of the bug.

**To Reproduce**
1. Launch the application
2. Select screen '...'
3. Start monitoring
4. Error occurs

**Expected Behavior**
What you expected to happen.

**Environment**
- OS: [e.g., Windows 11, Ubuntu 22.04]
- Python: [e.g., 3.11.5]
- Game: [e.g., Elden Ring]

**Additional Context**
Screenshots, logs, or other relevant information.
```

## 💡 Feature Requests

We welcome suggestions for:
- **New game support** (other FromSoftware titles)
- **UI improvements**
- **Performance optimizations**
- **Additional languages**

## 🎮 Adding New Game Support

To add support for a new game:

1. **Identify death messages**: Find the exact text displayed
2. **Add to detection list**: Update `death_messages` in both files
3. **Test thoroughly**: Ensure detection works reliably
4. **Update documentation**: Add game to README.md

Example:
```python
death_messages = [
    # Existing messages...
    
    # New game - Your Game Name
    "GAME OVER", "YOU ARE DEAD",
    # Variations
    "GAME  OVER", "GAMEOVER",
]
```

## 📝 Code Style Guidelines

### Python Code
- Use **English** for all variables, functions, and comments
- Follow **PEP 8** style guide
- Use **descriptive names**: `death_counter` not `cnt`
- Add **docstrings** for functions
- Handle **exceptions** gracefully

### Git Commits
Use conventional commit format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code formatting
- `refactor:` Code restructuring
- `test:` Adding tests

Examples:
```bash
git commit -m "feat: add Sekiro death message support"
git commit -m "fix: improve OCR accuracy for 4K displays"
git commit -m "docs: update installation instructions"
```

## 🧪 Testing

Before submitting:

1. **Test both versions**: GUI and terminal
2. **Test on your OS**: Ensure compatibility
3. **Test different games**: If adding game support
4. **Check edge cases**: Low resolution, multiple monitors
5. **Verify no regressions**: Existing features still work

## 🏷️ Release Process

For maintainers:

1. **Update CHANGELOG.md**
2. **Bump version** in relevant files
3. **Create release tag**: `git tag -a v1.0.0 -m "Release v1.0.0"`
4. **Push tag**: `git push origin v1.0.0`
5. **Create GitHub release** with changelog

## 📞 Get Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: [Your contact if desired]

## 🙏 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- CHANGELOG.md

Thank you for helping make Death Counter better! 🚀
