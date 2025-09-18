# Project Structure

This document outlines the professional structure of the AI Object Detection Web App.

## 📁 Directory Structure

```
Object-Detection/
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # MIT License
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 .gitignore                   # Git ignore rules
├── 📄 requirements.txt             # Production dependencies
├── 📄 requirements-dev.txt         # Development dependencies
├── 📄 docker-compose.yml           # Docker orchestration
├── 📄 Dockerfile.backend           # Backend container config
├── 📄 Dockerfile.frontend          # Frontend container config
├── 📄 PROJECT_STRUCTURE.md         # This file
│
├── 🖥️  backend/                    # FastAPI REST API
│   ├── main.py                     # API endpoints and ML logic
│   └── models/                     # Cached AI models (gitignored)
│
├── 🎨 frontend/                    # Flask web application
│   ├── app.py                      # Web interface logic
│   ├── templates/                  # HTML templates
│   │   ├── base.html              # Base template with Bootstrap
│   │   ├── index.html             # Upload interface
│   │   ├── results.html           # Single image results
│   │   └── batch_results.html     # Batch processing results
│   └── uploads/                   # User uploads (gitignored)
│
├── 📁 assets/                      # Demo images and screenshots
│   ├── Dashboard.png              # Dashboard screenshot
│   └── sample_images/             # Sample test images
│
├── 🔧 scripts/                     # Utility and setup scripts
│   ├── setup.py                   # Automated project setup
│   ├── download_models.py         # Model download utility
│   ├── start_backend.py           # Backend startup script
│   └── start_frontend.py          # Frontend startup script
│
├── 📚 docs/                        # Additional documentation
│   ├── API.md                     # API reference documentation
│   └── DEPLOYMENT.md              # Deployment guide
│
├── 🔒 .git/                        # Git repository (hidden)
├── 🚫 venv/                        # Virtual environment (gitignored)
└── 🚫 models/                      # AI model cache (gitignored)
```

## 📋 File Descriptions

### Root Files
- **README.md**: Comprehensive project documentation with badges, features, and usage
- **LICENSE**: MIT license for open source distribution
- **CONTRIBUTING.md**: Guidelines for contributors
- **.gitignore**: Excludes unnecessary files from version control
- **requirements.txt**: Production Python dependencies
- **requirements-dev.txt**: Development and testing dependencies
- **docker-compose.yml**: Multi-container Docker configuration
- **Dockerfile.backend**: Backend container build instructions
- **Dockerfile.frontend**: Frontend container build instructions

### Backend (`backend/`)
- **main.py**: FastAPI application with ML inference endpoints
- **models/**: Cached DETR models (auto-created, gitignored)

### Frontend (`frontend/`)
- **app.py**: Flask web application with upload and display logic
- **templates/**: Responsive HTML templates using Bootstrap 5
  - **base.html**: Common layout and styling
  - **index.html**: File upload interface with drag-and-drop
  - **results.html**: Single image detection results with bounding boxes
  - **batch_results.html**: Batch processing results with export options
- **uploads/**: Temporary file storage (gitignored)

### Assets (`assets/`)
- **Dashboard.png**: Application screenshot for README
- **sample_images/**: Test images for demonstration

### Scripts (`scripts/`)
- **setup.py**: One-command project setup and initialization
- **download_models.py**: Pre-download AI models for offline use
- **start_backend.py**: Backend server startup with proper paths
- **start_frontend.py**: Frontend server startup with proper paths

### Documentation (`docs/`)
- **API.md**: Complete API reference with examples
- **DEPLOYMENT.md**: Production deployment guide for various platforms

## 🔧 Configuration Files

### Python Dependencies
- **requirements.txt**: Core dependencies for production
- **requirements-dev.txt**: Additional tools for development

### Docker Configuration
- **docker-compose.yml**: Multi-service orchestration
- **Dockerfile.backend**: Optimized backend container
- **Dockerfile.frontend**: Lightweight frontend container

### Git Configuration
- **.gitignore**: Comprehensive exclusion rules for Python, IDEs, and project-specific files

## 🚀 Quick Commands

```bash
# Setup project
python scripts/setup.py

# Start development servers
python scripts/start_backend.py    # Terminal 1
python scripts/start_frontend.py   # Terminal 2

# Docker deployment
docker-compose up --build

# Install development tools
pip install -r requirements-dev.txt

# Run tests (when implemented)
pytest

# Code formatting
black .
isort .
```

## 🔒 Security Considerations

### Gitignored Items
- Virtual environments (`venv/`, `env/`)
- Model caches (`models/`, `*/models/`)
- User uploads (`uploads/`, `*/uploads/`)
- IDE configurations (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Python cache (`__pycache__/`, `*.pyc`)
- Environment variables (`.env`)

### Production Security
- Non-root Docker users
- Input validation and sanitization
- File type and size restrictions
- HTTPS enforcement (in deployment)
- Rate limiting (configurable)

## 📊 Professional Standards

### Code Organization
- ✅ Separation of concerns (backend/frontend)
- ✅ Modular architecture
- ✅ Clear naming conventions
- ✅ Comprehensive documentation
- ✅ Docker containerization
- ✅ Environment-specific configurations

### Development Workflow
- ✅ Version control with Git
- ✅ Dependency management
- ✅ Automated setup scripts
- ✅ Development and production environments
- ✅ Contribution guidelines
- ✅ Open source licensing

### Documentation Quality
- ✅ README with badges and clear instructions
- ✅ API documentation with examples
- ✅ Deployment guides for multiple platforms
- ✅ Contributing guidelines
- ✅ Code comments and docstrings

This structure follows industry best practices for Python web applications and provides a solid foundation for both development and production deployment.
