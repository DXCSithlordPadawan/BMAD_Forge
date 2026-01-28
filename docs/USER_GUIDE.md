# BMAD Forge User Guide

**Version:** 1.3.0  
**Last Updated:** January 2026

## Table of Contents

1. [Introduction](#1-introduction)
2. [Getting Started](#2-getting-started)
3. [Dashboard Overview](#3-dashboard-overview)
4. [Template Library](#4-template-library)
5. [Generate Document Feature](#5-generate-document-feature)
6. [Prompt Generation](#6-prompt-generation)
7. [BMAD Validation](#7-bmad-validation)
8. [History Management](#8-history-management)
9. [GitHub Synchronization](#9-github-synchronization)
10. [Frequently Asked Questions](#10-frequently-asked-questions)

---

## 1. Introduction

### What is BMAD Forge?

BMAD Forge is a web-based prompt engineering tool designed to help teams create, validate, and manage prompts that comply with the BMAD (Breakthrough Method for Agile AI-Driven Development) Framework. The application provides a centralized platform for working with AI coding assistants, enabling the creation of structured, consistent, and high-quality prompts.

### Key Features

- **Template Library**: Browse and filter 15+ BMAD templates by agent role and workflow phase
- **Generate Document**: Interactive wizard for creating documents section-by-section with real-time validation
- **Dynamic Forms**: Auto-generated input forms based on template variables
- **BMAD Compliance**: Automated validation for required sections and unreplaced variables
- **Real-time Validation**: Immediate feedback during prompt generation with 100% detection rate
- **History Management**: Track and review all generated prompts
- **GitHub Sync**: Import templates from remote repositories

### BMAD Framework Requirements

All generated prompts must include these required sections:
- **## Your Role** - Defines the AI assistant's persona and expertise
- **## Input** - Specifies the input data or context provided
- **## Output Requirements** - Describes the expected output format and structure

---

## 2. Getting Started

### Accessing the Application

1. Navigate to BMAD Forge in your web browser (default: http://localhost:8000)
2. You'll land on the Dashboard showing:
   - Total template count
   - Recent prompts
   - Quick action buttons

### First Steps

1. **Browse Templates**: Click "Templates" in the navigation bar to see available templates
2. **Generate a Document**: Use the "Generate Document" menu to create a document step-by-step
3. **Review History**: Check "History" to see previously generated prompts

---

## 3. Dashboard Overview

The Dashboard provides a comprehensive overview of your prompt engineering activities.

### Statistics Cards

- **Total Templates**: Number of active templates available
- **Recent Prompts**: Count of recently generated prompts
- **Agent Roles**: Number of different agent roles represented
- **Workflow Phases**: Number of different workflow phases covered

### Recent Activity

- **Recent Templates**: Quick access to the 5 most recently added templates
- **Recent Prompts**: View the 5 most recently generated prompts with validation status

### Quick Actions

Access key features with one click:
- Browse Templates
- Generate Document
- Sync from GitHub
- View History

---

## 4. Template Library

### Browsing Templates

The Template Library displays all available BMAD templates in a grid layout.

### Filtering Options

- **Agent Role**: Filter by role (Orchestrator, Analyst, PM, Architect, etc.)
- **Workflow Phase**: Filter by phase (Planning, Development)
- **Search**: Full-text search across template titles, descriptions, and content

### Template Cards

Each template card displays:
- Agent role badge
- Workflow phase badge
- Template title
- Brief description
- Variable count
- Action buttons (Preview, Generate)

### Template Details

Click "Preview" to view:
- Full template content
- List of variables
- Metadata (role, phase, version)

---

## 5. Generate Document Feature

### Overview

The **Generate Document** feature provides an interactive wizard that guides you through creating a document section-by-section. This approach ensures:

- 95%+ compliance rate for generated prompts
- Real-time validation feedback
- Step-by-step guidance

### How to Use

1. **Select a Template**
   - Navigate to "Generate Document" in the menu
   - Browse available templates using filters
   - Click "Generate" on your chosen template

2. **Follow the Wizard**
   - The wizard presents each section one at a time
   - Fill in required variables for each section
   - Add your custom content
   - Review real-time validation feedback

3. **Navigate Steps**
   - Use "Previous" to go back and edit
   - Use "Next" to proceed to the next section
   - A progress indicator shows your current position

4. **Generate Document**
   - After completing all sections, click "Generate Document"
   - Review the final output with validation results
   - Copy to clipboard or download the result

### Real-time Validation

As you enter content, the system provides immediate feedback:

- **✅ Green**: Content looks good, no issues detected
- **⚠️ Yellow**: Warnings (e.g., short content, missing suggestions)
- **❌ Red**: Issues that need attention (e.g., unreplaced variables)

### Validation Checks Performed

The wizard performs these checks in real-time:

| Check | Detection Rate | Description |
|-------|----------------|-------------|
| Unreplaced Variables | 100% | Detects any `{{variable}}` or `[variable]` syntax not replaced |
| Missing Sections | 100% | Ensures all required sections are present |
| Content Length | Advisory | Warns if section content is too short |
| Content Quality | Advisory | Suggests improvements based on section type |

---

## 6. Prompt Generation

### Standard Form-Based Generation

For simpler templates, you can use the standard prompt generation:

1. Select a template from the Template Library
2. Click "Generate Prompt"
3. Fill in all required variables in the form
4. Click "Generate"
5. Review the result with validation status

### Variable Syntax

BMAD Forge supports two variable syntaxes:
- Double braces: `{{VARIABLE_NAME}}`
- Square brackets: `[VARIABLE_NAME]`

### Best Practices

1. **Be Specific**: Provide detailed, specific values for variables
2. **Check Validation**: Review all validation warnings before using the prompt
3. **Save History**: Generated prompts are automatically saved for future reference

---

## 7. BMAD Validation

### Overview

BMAD Forge validates all generated prompts against BMAD Framework requirements to ensure quality and consistency.

### Validation Goals

- **95% compliance rate** for prompts generated through the platform
- **100% detection rate** for missing required sections
- **100% detection rate** for unreplaced template variables
- **< 5% false positive rate** for validation warnings

### Required Sections

Every BMAD-compliant prompt must include:

1. **## Your Role**
   - Defines who the AI should act as
   - Should include responsibilities and expertise

2. **## Input**
   - Specifies what information is being provided
   - Should describe the context and data

3. **## Output Requirements**
   - Describes expected output format
   - Should include structure and specifications

### Optional Sections (Recommended)

- **## Context**: Additional background information
- **## Constraints**: Limitations or requirements
- **## Examples**: Sample outputs or reference materials
- **## Step-by-Step Instructions**: Detailed guidance
- **## Success Criteria**: How to evaluate the output
- **## Notes**: Additional considerations

### Validation Indicators

| Indicator | Meaning |
|-----------|---------|
| ✅ BMAD Compliant | All requirements met |
| ❌ Needs Review | Issues detected - review and fix |

### Validation Report

Each generated prompt includes a detailed validation report showing:
- Overall compliance status
- Missing sections (if any)
- Unreplaced variables (if any)
- Compliance score
- Specific issues to address

---

## 8. History Management

### Viewing History

Access prompt history from "History" in the navigation bar.

### Features

- **Chronological List**: View all generated prompts sorted by date
- **Validation Status**: See at a glance which prompts are valid
- **Filter by Status**: Filter to show only valid or invalid prompts
- **Template Reference**: See which template was used

### Actions

From the history view, you can:
- View the full generated prompt
- Download as a text file
- Copy to clipboard
- Regenerate from the same template

---

## 9. GitHub Synchronization

### Overview

BMAD Forge can sync templates from GitHub repositories, enabling teams to share and version-control their templates.

### Default Repository

The default template repository is configured in `config.yaml`:
```yaml
templates:
  github:
    repository: "DXCSithlordPadawan/BMAD_Forge"
    branch: "main"
    remote_path: "aitrg/templates"
```

### Manual Sync

1. Navigate to "Sync" in the navigation bar
2. Enter the repository URL
3. Specify the path to templates
4. Select the branch
5. Click "Sync"

### Sync Results

After syncing, you'll see:
- Number of templates created
- Number of templates updated
- Any errors encountered

### Recursive Search

The sync feature recursively searches all subfolders for templates, making it easy to organize templates in nested directory structures.

---

## 10. Frequently Asked Questions

### General Questions

**Q: What is the BMAD Framework?**
A: BMAD (Breakthrough Method for Agile AI-Driven Development) is a methodology for structuring effective prompts for AI coding assistants.

**Q: Do I need to install anything?**
A: BMAD Forge is a web application. Once deployed, you only need a web browser.

**Q: Can I create my own templates?**
A: Yes, templates can be created manually or synced from GitHub repositories.

### Template Questions

**Q: What variable syntax should I use?**
A: Both `{{VARIABLE_NAME}}` and `[VARIABLE_NAME]` are supported.

**Q: How do I add new templates?**
A: Either sync from a GitHub repository or add template files to the `forge/templates/agents/` directory.

**Q: What makes a template BMAD-compliant?**
A: Templates must include ## Your Role, ## Input, and ## Output Requirements sections.

### Validation Questions

**Q: What causes a "Needs Review" status?**
A: Missing required sections, unreplaced variables, or other validation issues.

**Q: How can I fix unreplaced variables?**
A: Ensure all `{{variable}}` or `[variable]` patterns are filled with actual values.

**Q: What is the false positive rate for warnings?**
A: The validation system targets < 5% false positive rate for warnings.

### Generate Document Questions

**Q: What's the difference between "Generate Prompt" and "Generate Document"?**
A: "Generate Prompt" uses a simple form. "Generate Document" provides a step-by-step wizard with real-time validation for each section.

**Q: Can I go back to edit previous sections?**
A: Yes, use the "Previous" button or click on completed steps in the progress indicator.

**Q: How is my progress saved?**
A: Section data is saved in your session as you progress through the wizard.

### Technical Questions

**Q: What browsers are supported?**
A: BMAD Forge works with all modern browsers (Chrome, Firefox, Safari, Edge).

**Q: Can I use BMAD Forge offline?**
A: The application requires network access to the server, but GitHub sync is optional.

**Q: Where is my data stored?**
A: Generated prompts and templates are stored in the database (SQLite by default).

---

## Support

For additional help or to report issues:
- Check the [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Review the [README_WEBAPP.md](../webapp/README_WEBAPP.md) for setup instructions
- Consult the [BMAD Framework](https://github.com/bmadcode/BMAD-METHOD-v5) documentation

---

*This user guide is part of the BMAD Forge documentation suite.*
