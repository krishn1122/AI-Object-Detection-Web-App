# Contributing to AI Object Detection Web App

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/Object-Detection.git
   cd Object-Detection
   ```
3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python scripts/setup.py
   ```

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- 4GB+ RAM
- Internet connection (for model downloads)

### Local Development
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

2. **Start development servers**
   ```bash
   # Terminal 1: Backend
   python scripts/start_backend.py
   
   # Terminal 2: Frontend
   python scripts/start_frontend.py
   ```

3. **Access the application**
   - Frontend: http://localhost:5000
   - API Docs: http://localhost:8000/docs

## 📝 Code Style

### Python Code Style
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions and classes
- Maximum line length: 88 characters (Black formatter)

### Frontend Code Style
- Use semantic HTML
- Follow Bootstrap conventions
- Keep JavaScript modular
- Use meaningful variable names

### Example Code Style
```python
def detect_objects(
    image: Image.Image, 
    confidence_threshold: float = 0.7
) -> List[Dict[str, Any]]:
    """
    Detect objects in an image using DETR model.
    
    Args:
        image: PIL Image object
        confidence_threshold: Minimum confidence score (0.0-1.0)
        
    Returns:
        List of detected objects with bounding boxes
    """
    # Implementation here
    pass
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=backend --cov=frontend

# Run specific test file
python -m pytest tests/test_api.py
```

### Writing Tests
- Write tests for new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test both success and error cases

## 📋 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   python -m pytest
   python scripts/start_backend.py  # Test backend
   python scripts/start_frontend.py  # Test frontend
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format
Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## 🐛 Bug Reports

When reporting bugs, please include:
- **Environment details** (OS, Python version, browser)
- **Steps to reproduce** the issue
- **Expected behavior**
- **Actual behavior**
- **Screenshots** if applicable
- **Error messages** or logs

## 💡 Feature Requests

For feature requests, please provide:
- **Clear description** of the feature
- **Use case** or problem it solves
- **Proposed solution** (if you have one)
- **Alternative solutions** considered

## 🏗️ Architecture Guidelines

### Backend (FastAPI)
- Keep endpoints focused and single-purpose
- Use proper HTTP status codes
- Implement proper error handling
- Add input validation
- Document API endpoints

### Frontend (Flask)
- Keep templates modular
- Use progressive enhancement
- Implement proper error handling
- Make UI responsive
- Follow accessibility guidelines

### General
- Write self-documenting code
- Use meaningful variable names
- Keep functions small and focused
- Avoid deep nesting
- Handle edge cases

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Update API documentation
- Include code examples
- Keep documentation up-to-date

## 🤝 Code Review

All contributions go through code review:
- Be respectful and constructive
- Address all feedback
- Keep discussions focused on the code
- Be open to suggestions

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

## 📞 Getting Help

- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Email**: Contact maintainers directly

Thank you for contributing! 🎉
