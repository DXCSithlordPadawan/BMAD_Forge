# BMAD Forge

A Django-based web application for prompt engineering using the BMAD (Breakthrough Method for Agile AI-Driven Development) Framework. Generate, validate, and manage BMAD-compliant prompts for AI coding assistants.

## Features

- **Template Library**: Browse and filter BMAD templates by agent role and workflow phase
- **Dynamic Forms**: Auto-generated forms based on template variables
- **Prompt Generation**: Generate BMAD-compliant prompts with variable substitution
- **BMAD Validation**: Validate generated prompts against framework requirements
- **GitHub Sync**: Import templates from remote GitHub repositories
- **History Management**: Track and review previously generated prompts
- **Export Options**: Copy to clipboard or download prompts as text files

## BMAD Framework Support

BMAD Forge supports all standard BMAD agent roles and workflow phases:

### Agent Roles
- **Orchestrator**: Coordination and oversight
- **Analyst**: Requirements and data analysis
- **Project Manager**: Planning and tracking
- **Architect**: System design and architecture
- **Scrum Master**: Agile process facilitation
- **Developer**: Implementation and coding
- **QA Engineer**: Testing and quality assurance

### Workflow Phases
- **Planning Phase**: Requirements, analysis, planning
- **Development Phase**: Implementation, testing, deployment

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bmad_forge
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

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Open your browser and navigate to:
```
http://localhost:8000
```

### Syncing Templates

After starting the server, sync templates from GitHub:

1. Navigate to the Sync page (`/sync/`)
2. Enter the repository URL (or use the default)
3. Click "Sync Templates"

Default repository: `DXCSithlordPadawan/training` (path: `aitrg/templates`)

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Django secret key | Auto-generated |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `GITHUB_TOKEN` | GitHub personal access token | (empty) |
| `TEMPLATE_REPO` | Repository for templates | `DXCSithlordPadawan/training` |

### Database Configuration

For MVP, BMAD Forge uses SQLite by default. For production, configure PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bmad_forge',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Project Structure

```
bmad_forge/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── bmad_forge/           # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── forge/                # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── forms.py          # Form classes
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin configuration
│   ├── services/         # Business logic
│   │   ├── github_sync.py
│   │   ├── template_parser.py
│   │   └── bmad_validator.py
│   ├── templates/        # HTML templates
│   └── static/           # CSS and JavaScript
└── tests/                # Test suite
    ├── test_models.py
    ├── test_views.py
    └── test_services.py
```

## Usage

### Creating a Prompt

1. Browse the template library
2. Select a template matching your needs
3. Fill in the dynamic form with required values
4. Click "Generate Prompt"
5. Review the generated prompt
6. Copy or download the result

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

### BMAD Compliance

Generated prompts are validated for:
- Required sections (Your Role, Input, Output Requirements)
- Complete variable substitution
- Meaningful content length
- Proper structure

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

### Example Production Settings

```python
import os

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- [BMAD Framework](https://github.com/bmadcode/BMAD-METHOD-v5) for the methodology
- [Django](https://www.djangoproject.com/) for the web framework
- [Bootstrap 5](https://getbootstrap.com/) for the UI components
