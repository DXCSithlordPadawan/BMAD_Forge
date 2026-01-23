"""
Tests for BMAD Forge services.
"""

import pytest
from forge.services import TemplateParser, BMADValidator, GitHubSyncService


class TestTemplateParser:
    """Tests for the TemplateParser service."""
    
    def test_extract_variables_simple(self):
        """Test basic variable extraction."""
        content = "Hello {{name}}, welcome to {{place}}."
        variables = TemplateParser.extract_variables_simple(content)
        
        assert len(variables) == 2
        assert 'name' in variables
        assert 'place' in variables
    
    def test_extract_variables_mixed_syntax(self):
        """Test extracting mixed variable syntax."""
        content = "{{double}} and [single] and {{another}}"
        variables = TemplateParser.extract_variables_simple(content)
        
        assert len(variables) == 3
        assert 'double' in variables
        assert 'single' in variables
        assert 'another' in variables
    
    def test_extract_variables_with_defaults(self):
        """Test extracting variables with default values."""
        content = "{{name:John}} {{email:john@example.com}}"
        variables = TemplateParser.extract_variables_simple(content)
        
        assert len(variables) == 2
        assert 'name' in variables
        assert 'email' in variables
    
    def test_detect_sections(self):
        """Test section detection."""
        content = """
## Your Role
You are a developer.

## Input
Some input

## Output Requirements
Format output
"""
        sections = TemplateParser.detect_sections(content)
        
        assert '## Your Role' in sections
        assert '## Input' in sections
        assert '## Output Requirements' in sections
    
    def test_check_required_sections_all_present(self):
        """Test required sections check when all present."""
        content = """
## Your Role
Developer

## Input
Task description

## Output Requirements
Format requirements
"""
        is_valid, missing = TemplateParser.check_required_sections(content)
        
        assert is_valid is True
        assert len(missing) == 0
    
    def test_check_required_sections_missing(self):
        """Test required sections check when some missing."""
        content = """
## Your Role
Developer
"""
        is_valid, missing = TemplateParser.check_required_sections(content)
        
        assert is_valid is False
        assert len(missing) == 2
        assert '## Input' in missing
        assert '## Output Requirements' in missing
    
    def test_substitute_variables(self):
        """Test variable substitution."""
        content = "Hello {{name}}, you work at {{company}}."
        values = {'name': 'Alice', 'company': 'ACME'}
        
        result = TemplateParser.substitute_variables(content, values)
        
        assert result == "Hello Alice, you work at ACME."
    
    def test_find_unreplaced_variables(self):
        """Test finding unreplaced variables."""
        content = "Hello {{name}}, {{greeting}}!"
        values = {'name': 'Alice'}  # greeting not provided
        
        unreplaced = TemplateParser.find_unreplaced_variables(
            TemplateParser.substitute_variables(content, values)
        )
        
        assert 'greeting' in unreplaced
    
    def test_validate_template_valid(self):
        """Test template validation with valid template."""
        content = """
## Your Role
You are a developer.

## Input
Build a feature.

## Output Requirements
Provide code with tests.
"""
        result = TemplateParser.validate_template(content)
        
        assert result['is_valid'] is True
        assert len(result['errors']) == 0
    
    def test_validate_template_missing_sections(self):
        """Test template validation with missing sections."""
        content = "# Just a title"
        result = TemplateParser.validate_template(content)
        
        assert result['is_valid'] is False
        assert len(result['errors']) > 0


class TestBMADValidator:
    """Tests for the BMADValidator service."""
    
    def test_validate_valid_prompt(self):
        """Test validating a BMAD-compliant prompt."""
        prompt = """
## Your Role
You are an experienced software developer.

## Input
Implement a user authentication system with the following requirements:
- User registration
- Login/logout
- Password reset

## Output Requirements
Provide the following:
1. Complete source code
2. Unit tests with 80% coverage
3. Documentation
4. Integration instructions
"""
        report = BMADValidator.validate(prompt)
        
        assert report.is_valid is True
        assert report.score > 0
    
    def test_validate_missing_role_section(self):
        """Test validation fails without Your Role section."""
        prompt = """
## Input
Some task

## Output Requirements
Output format
"""
        report = BMADValidator.validate(prompt)
        
        assert report.is_valid is False
        assert '## Your Role' in report.missing_sections
    
    def test_validate_with_unreplaced_variables(self):
        """Test validation fails with unreplaced variables."""
        prompt = """
## Your Role
You are {{role}}.

## Input
{{task}}

## Output Requirements
Provide results.
"""
        report = BMADValidator.validate(prompt)
        
        assert report.is_valid is False
        assert len(report.unreplaced_variables) > 0
    
    def test_quick_validate_valid(self):
        """Test quick validation for valid prompt."""
        prompt = """
## Your Role
Developer

## Input
Task

## Output Requirements
Format
"""
        is_valid, issues = BMADValidator.quick_validate(prompt)
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_quick_validate_invalid(self):
        """Test quick validation for invalid prompt."""
        prompt = "Just some text"
        is_valid, issues = BMADValidator.quick_validate(prompt)
        
        assert is_valid is False
        assert len(issues) > 0


class TestGitHubSyncService:
    """Tests for the GitHubSyncService."""
    
    def test_detect_agent_role_from_filename(self):
        """Test agent role detection from filename."""
        service = GitHubSyncService()
        
        assert service.detect_agent_role('content', 'developer_template.md') == 'developer'
        assert service.detect_agent_role('content', 'analyst_report.md') == 'analyst'
        assert service.detect_agent_role('content', 'pm_planning.md') == 'pm'
    
    def test_detect_workflow_phase_from_filename(self):
        """Test workflow phase detection from filename."""
        service = GitHubSyncService()
        
        assert service.detect_workflow_phase('content', 'planning_template.md') == 'planning'
        assert service.detect_workflow_phase('content', 'development_sprint.md') == 'development'
    
    def test_parse_template_description(self):
        """Test description extraction from template."""
        service = GitHubSyncService()
        
        content = """This is a brief description.

More details here.

## Your Role
..."""
        description = service.parse_template_description(content)
        
        assert 'brief description' in description
        assert '## Your Role' not in description
    
    def test_init_with_token(self):
        """Test service initialization with token."""
        service = GitHubSyncService(token='test-token')
        
        assert service.token == 'test-token'
        assert 'Authorization' in service.headers


class TestDocumentGenerator:
    """Tests for the DocumentGenerator service."""
    
    def test_extract_sections(self):
        """Test extracting sections from template content."""
        from forge.services import DocumentGenerator
        
        content = """# Document Title

## Section One
Content for section one.

## Section Two
Content for section two.

### Subsection
More content here.
"""
        sections = DocumentGenerator.extract_sections(content)
        
        assert len(sections) >= 3
        section_names = [s.name for s in sections]
        assert 'Document Title' in section_names
        assert 'Section One' in section_names
        assert 'Section Two' in section_names
    
    def test_validate_section_content_valid(self):
        """Test section validation with valid content."""
        from forge.services import DocumentGenerator
        
        result = DocumentGenerator.validate_section_content(
            "Your Role",
            "You are an experienced software developer with responsibility for implementing features."
        )
        
        assert result.is_valid is True
        assert len(result.unreplaced_variables) == 0
    
    def test_validate_section_content_with_unreplaced_variables(self):
        """Test section validation detects unreplaced variables (100% detection requirement)."""
        from forge.services import DocumentGenerator
        
        result = DocumentGenerator.validate_section_content(
            "Input",
            "Process the {{file_name}} and analyze the [data_source]."
        )
        
        assert result.is_valid is False
        assert 'file_name' in result.unreplaced_variables
        assert 'data_source' in result.unreplaced_variables
    
    def test_validate_section_content_short_content(self):
        """Test section validation warns about short content."""
        from forge.services import DocumentGenerator
        
        result = DocumentGenerator.validate_section_content(
            "Context",
            "Brief."
        )
        
        # Should have warnings about short content
        assert len(result.warnings) > 0
    
    def test_get_wizard_steps(self):
        """Test generating wizard steps from template content."""
        from forge.services import DocumentGenerator
        
        content = """## Your Role
You are a developer.

## Input
Task description.

## Output Requirements
Format specifications.
"""
        steps = DocumentGenerator.get_wizard_steps(content)
        
        assert len(steps) == 3
        assert steps[0]['section_name'] == 'Your Role'
        assert steps[1]['section_name'] == 'Input'
        assert steps[2]['section_name'] == 'Output Requirements'
    
    def test_validate_document_compliance_valid(self):
        """Test document compliance validation with valid content."""
        from forge.services import DocumentGenerator
        
        content = """## Your Role
You are an experienced software developer.

## Input
Build a user authentication system.

## Output Requirements
Provide complete source code with tests.
"""
        report = DocumentGenerator.validate_document_compliance(content)
        
        assert report['is_compliant'] is True
        assert len(report['missing_sections']) == 0
        assert len(report['unreplaced_variables']) == 0
    
    def test_validate_document_compliance_missing_sections(self):
        """Test document compliance validation detects missing sections."""
        from forge.services import DocumentGenerator
        
        content = """## Your Role
Just a partial document.
"""
        report = DocumentGenerator.validate_document_compliance(content)
        
        assert report['is_compliant'] is False
        assert '## Input' in report['missing_sections']
        assert '## Output Requirements' in report['missing_sections']
    
    def test_validate_document_compliance_unreplaced_variables(self):
        """Test document compliance validation detects unreplaced variables (100% detection)."""
        from forge.services import DocumentGenerator
        
        content = """## Your Role
You are {{role_name}}.

## Input
Process {{input_data}}.

## Output Requirements
Return formatted output.
"""
        report = DocumentGenerator.validate_document_compliance(content)
        
        assert report['is_compliant'] is False
        assert 'role_name' in report['unreplaced_variables']
        assert 'input_data' in report['unreplaced_variables']
