# BMAD_Forge
WEB application to help create BMAD prompts
Plan for the creation of a Django-based web application called "BMAD Forge" that serves as a prompt engineering tool for generating BMAD (Breakthrough Method for Agile AI-Driven Development) Framework-compliant prompts.

## Requirements:

### 1. Framework Integration
- Reference the BMAD-METHOD-v5 framework from: https://github.com/bmadcode/BMAD-METHOD-v5
- Support BMAD agent roles: Analyst, PM, Architect, Scrum Master, Developer, QA, Orchestrator
- Support BMAD workflow phases: Planning Phase, Development Phase

### 2. Template Management
- Load templates from GitHub repository: https://github.com/DXCSithlordPadawan/training/tree/main/aitrg/templates
- Support template variable syntax: {{VARIABLE_NAME}} and [VARIABLE_NAME]
- Auto-detect agent role and workflow phase from template content
- Store templates in database with metadata (title, agent_role, workflow_phase, remote_url)

### 3. Core Features
- Dashboard displaying template count and recent generated prompts
- Template library with filtering by agent role and workflow phase
- Dynamic form generation based on template variables
- Prompt generation with variable substitution
- BMAD compliance validation checking for:
  - Required sections: ## Your Role, ## Input, ## Output Requirements
  - Complete variable substitution (no unreplaced placeholders)
- Copy to clipboard and download functionality
- GitHub sync to import/update templates from remote repositories

### 4. Technical Stack
- Backend: Python 3.11+, Django 5.x
- Database: SQLite (MVP), PostgreSQL (production)
- Frontend: Bootstrap 5, custom CSS (dark theme)
- No user authentication required for MVP
- Responsive design

### 5. Database Models
- Template: title, content, agent_role, workflow_phase, remote_url, last_updated, is_active
- GeneratedPrompt: template (FK), input_data (JSON), final_output, is_valid, validation_notes, created_at

### 6. Pages Required
- Home/Dashboard
- Template List (with filters)
- Prompt Form (dynamic based on template)
- Generated Prompt View (with validation status, copy/download)
- GitHub Sync

### 7. Deliverables
- Complete Django project structure
- All models, views, forms, and templates
- Database migrations
- Sample BMAD templates pre-loaded
- Unit tests or Playwright tests
- README with setup and deployment instructions

## Success Criteria:
- Users can browse available templates organized by agent and phase
- Users can fill dynamic forms to generate BMAD-compliant prompts
- Generated prompts are validated against BMAD structural requirements
- Prompts can be copied or downloaded for use in AI coding assistants
