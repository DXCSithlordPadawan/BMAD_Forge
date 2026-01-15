# BMAD Forge Web Application

A Django-based web application for prompt engineering using the BMAD (Breakthrough Method for Agile AI-Driven Development) Framework. This application enables teams to generate, validate, and manage BMAD-compliant prompts for AI coding assistants.

## Overview

BMAD Forge is built according to the specifications in [BMAD_PRD.md](../BMAD_PRD.md) and provides a comprehensive platform for:

- **Template Management**: Browse and filter BMAD templates by agent role and workflow phase
- **Dynamic Forms**: Auto-generated forms based on template variables
- **Prompt Generation**: Generate BMAD-compliant prompts with variable substitution
- **BMAD Validation**: Validate generated prompts against framework requirements
- **GitHub Sync**: Import templates from remote GitHub repositories
- **History Management**: Track and review previously generated prompts
- **Export Options**: Copy to clipboard or download prompts as text files

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git

### Installation

1. Navigate to the webapp directory:
```bash
cd webapp
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
python manage.py migrate
```

6. Load initial templates:
```bash
python load_local_templates.py
```

7. Start the development server:
```bash
python manage.py runserver
```

8. Open your browser and navigate to:
```
http://localhost:8000
```

## Features

### BMAD Framework Support

The application supports all standard BMAD agent roles and workflow phases:

#### Agent Roles
- **Orchestrator**: Coordination and oversight
- **Analyst**: Requirements and data analysis
- **Project Manager**: Planning and tracking
- **Architect**: System design and architecture
- **Scrum Master**: Agile process facilitation
- **Developer**: Implementation and coding
- **QA Engineer**: Testing and quality assurance

#### Workflow Phases
- **Planning Phase**: Requirements, analysis, planning
- **Development Phase**: Implementation, testing, deployment

### Template Management

The template library provides:
- Card-based grid layout with responsive design
- Filtering by agent role and workflow phase
- Full-text search across titles and descriptions
- Template detail views with metadata
- Variable detection and display

### Prompt Generation

Dynamic form generation includes:
- Automatic field generation based on template variables
- Smart field types (text input vs textarea)
- Real-time validation
- Template preview
- Variable substitution

### BMAD Validation

Generated prompts are validated for:
- Required sections (Your Role, Input, Output Requirements)
- Complete variable substitution
- Content structure and quality
- Compliance scoring

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Django secret key | Auto-generated |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `GITHUB_TOKEN` | GitHub personal access token | (empty) |
| `TEMPLATE_REPO` | Repository for templates | `DXCSithlordPadawan/BMAD_Forge` |

### Database Configuration

For MVP, BMAD Forge uses SQLite by default (no configuration needed). For production, configure PostgreSQL in your `.env` file or `settings.py`.

## Project Structure

```
webapp/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore patterns
├── README.md             # This file
├── load_local_templates.py  # Script to load templates
├── bmad_forge/           # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py          # Root URL configuration
│   └── wsgi.py          # WSGI application
├── forge/               # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── forms.py         # Form classes
│   ├── urls.py          # URL routing
│   ├── admin.py         # Admin configuration
│   ├── services/        # Business logic
│   │   ├── github_sync.py
│   │   ├── template_parser.py
│   │   └── bmad_validator.py
│   ├── templates/       # HTML templates and prompt templates
│   │   ├── forge/       # Django HTML templates
│   │   └── agents/      # BMAD prompt templates
│   ├── static/          # CSS and JavaScript
│   └── management/      # Management commands
└── tests/               # Test suite
    ├── test_models.py
    ├── test_views.py
    └── test_services.py
```

## Usage

### Creating a Prompt

1. Browse the template library from the dashboard
2. Select a template matching your needs
3. Fill in the dynamic form with required values
4. Click "Generate Prompt"
5. Review the generated prompt and validation results
6. Copy to clipboard or download the result

### Template Format

BMAD Forge templates use the following variable syntax:
- `{{VARIABLE_NAME}}` - Double brace syntax
- `[VARIABLE_NAME]` - Single bracket syntax

Example template:
```markdown
## Your Role
You are an experienced {{agent_role}} specializing in {{domain}}.

## Input
{{project_description}}

## Output Requirements
Provide a comprehensive {{deliverable}} that includes:
1. Key objectives
2. Implementation approach
3. Timeline
```

## Development

### Running Tests

```bash
pytest
```

Or with coverage:
```bash
pytest --cov=forge
```

### Creating Migrations

After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Management Commands

Sync templates from GitHub:
```bash
python manage.py sync_templates --owner owner --repo repo --path path
```

## Deployment

### Production Checklist

1. Set `DEBUG=False` in environment
2. Generate a strong `SECRET_KEY`
3. Configure a production database (PostgreSQL recommended)
4. Set up static file serving
5. Configure allowed hosts
6. Set up HTTPS/SSL certificate
7. Configure GitHub token for private repositories

### Docker Deployment (Optional)

A Dockerfile can be created for containerized deployment. The application is designed to work with standard Django deployment practices.

## Technology Stack

- **Backend**: Django 5.x, Python 3.11+
- **Frontend**: Bootstrap 5, vanilla JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **External Services**: GitHub API (for template synchronization)

## License

This project is part of the BMAD Framework ecosystem.

## Acknowledgments

- [BMAD Framework](https://github.com/bmadcode/BMAD-METHOD-v5) for the methodology
- [Django](https://www.djangoproject.com/) for the web framework
- [Bootstrap 5](https://getbootstrap.com/) for the UI components

## Support

For issues, questions, or contributions, please refer to the main repository documentation.
