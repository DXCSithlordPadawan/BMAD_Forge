# BMAD_Forge

A Django-based web application called "BMAD Forge" that serves as a prompt engineering tool for generating BMAD (Breakthrough Method for Agile AI-Driven Development) Framework-compliant prompts.

## 🚀 Quick Start

The web application is located in the `webapp/` directory. To get started:

```bash
cd webapp
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python load_local_templates.py
python manage.py runserver
```

Then visit http://localhost:8000

📖 **For complete documentation, see [webapp/README_WEBAPP.md](webapp/README_WEBAPP.md)**

## 📋 Product Requirements

This application implements the specifications defined in [BMAD_PRD.md](BMAD_PRD.md).

## ✨ Features

### Core Functionality
- **Dashboard** - Overview with statistics and quick actions
- **Template Library** - Browse and filter 15+ BMAD templates by agent role and workflow phase
- **Dynamic Forms** - Auto-generated input forms based on template variables
- **Prompt Generation** - Variable substitution with validation
- **BMAD Compliance** - Automated validation for required sections
- **History Management** - Track and review generated prompts
- **GitHub Sync** - Import templates from remote repositories

### Supported BMAD Elements

### Supported BMAD Elements

**Agent Roles:**
- Orchestrator - Coordination and oversight
- Analyst - Requirements and data analysis  
- Project Manager - Planning and tracking
- Architect - System design and architecture
- Scrum Master - Agile process facilitation
- Developer - Implementation and coding
- QA Engineer - Testing and quality assurance

**Workflow Phases:**
- Planning Phase - Requirements, analysis, estimation
- Development Phase - Implementation, testing, deployment

## 🏗️ Architecture

### Technical Stack
- **Backend**: Django 5.x, Python 3.11+
- **Frontend**: Bootstrap 5, vanilla JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **External Services**: GitHub API for template synchronization

### Project Structure
```
BMAD_Forge/
├── BMAD_PRD.md           # Product requirements document
├── README.md             # This file
├── bmad_forge/           # Original development version
└── webapp/              # Production web application ⭐
    ├── README_WEBAPP.md  # Detailed setup guide
    ├── manage.py
    ├── requirements.txt
    ├── bmad_forge/      # Django project config
    ├── forge/           # Main application
    └── tests/           # Test suite
```

## 📚 Documentation

- **[webapp/README_WEBAPP.md](webapp/README_WEBAPP.md)** - Complete setup and usage guide
- **[BMAD_PRD.md](BMAD_PRD.md)** - Detailed product requirements
- **[BMAD Framework](https://github.com/bmadcode/BMAD-METHOD-v5)** - Framework methodology

## 🎯 Use Cases

1. **Generate BMAD-Compliant Prompts** - Create structured prompts for AI coding assistants
2. **Template Management** - Organize and maintain reusable prompt templates
3. **Team Standardization** - Ensure consistent prompt quality across development teams
4. **GitHub Integration** - Sync templates from organizational repositories

## 🛠️ Development

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Git

### Local Development Setup
```bash
cd webapp
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python load_local_templates.py
python manage.py runserver
```

### Running Tests
```bash
cd webapp
pytest
```

## 🚢 Deployment

The application supports standard Django deployment patterns:
- Docker containerization
- WSGI/ASGI server deployment
- PostgreSQL for production database
- Static file serving via CDN

See [webapp/README_WEBAPP.md](webapp/README_WEBAPP.md) for detailed deployment instructions.

## 📝 License

This project is part of the BMAD Framework ecosystem.

## 🙏 Acknowledgments

- [BMAD Framework](https://github.com/bmadcode/BMAD-METHOD-v5) for the methodology
- [Django](https://www.djangoproject.com/) for the web framework
- [Bootstrap 5](https://getbootstrap.com/) for UI components

---

**Status**: ✅ Web application fully functional and ready for use
