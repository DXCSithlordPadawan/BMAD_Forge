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
    
    def test_fetch_directory_contents_recursive_files_only(self):
        """Test recursive fetch returns only files when directory has no subdirectories."""
        service = GitHubSyncService()
        
        # Mock fetch_directory_contents to return files only
        original_fetch = service.fetch_directory_contents
        service.fetch_directory_contents = lambda o, r, b, p: [
            {'name': 'file1.md', 'path': 'templates/file1.md', 'type': 'file'},
            {'name': 'file2.md', 'path': 'templates/file2.md', 'type': 'file'},
        ]
        
        result = service.fetch_directory_contents_recursive('owner', 'repo', 'main', 'templates')
        
        assert len(result) == 2
        assert all(item['type'] == 'file' for item in result)
        
        # Restore original method
        service.fetch_directory_contents = original_fetch
    
    def test_fetch_directory_contents_recursive_with_subdirectories(self):
        """Test recursive fetch traverses subdirectories and returns all files."""
        service = GitHubSyncService()
        
        # Track calls to verify recursion
        call_paths = []
        
        def mock_fetch(owner, repo, branch, path):
            call_paths.append(path)
            if path == 'templates':
                return [
                    {'name': 'file1.md', 'path': 'templates/file1.md', 'type': 'file'},
                    {'name': 'subdir', 'path': 'templates/subdir', 'type': 'dir'},
                ]
            elif path == 'templates/subdir':
                return [
                    {'name': 'file2.md', 'path': 'templates/subdir/file2.md', 'type': 'file'},
                    {'name': 'nested', 'path': 'templates/subdir/nested', 'type': 'dir'},
                ]
            elif path == 'templates/subdir/nested':
                return [
                    {'name': 'file3.md', 'path': 'templates/subdir/nested/file3.md', 'type': 'file'},
                ]
            return []
        
        service.fetch_directory_contents = mock_fetch
        
        result = service.fetch_directory_contents_recursive('owner', 'repo', 'main', 'templates')
        
        # Should have 3 files from all levels
        assert len(result) == 3
        file_paths = [f['path'] for f in result]
        assert 'templates/file1.md' in file_paths
        assert 'templates/subdir/file2.md' in file_paths
        assert 'templates/subdir/nested/file3.md' in file_paths
        
        # Verify all directories were traversed
        assert 'templates' in call_paths
        assert 'templates/subdir' in call_paths
        assert 'templates/subdir/nested' in call_paths
    
    def test_fetch_directory_contents_recursive_empty_directory(self):
        """Test recursive fetch handles empty directories gracefully."""
        service = GitHubSyncService()
        
        service.fetch_directory_contents = lambda o, r, b, p: []
        
        result = service.fetch_directory_contents_recursive('owner', 'repo', 'main', 'templates')
        
        assert result == []
    
    def test_fetch_directory_contents_recursive_mixed_content(self):
        """Test recursive fetch correctly filters files from mixed directory content."""
        service = GitHubSyncService()
        
        def mock_fetch(owner, repo, branch, path):
            if path == 'templates':
                return [
                    {'name': 'file1.md', 'path': 'templates/file1.md', 'type': 'file'},
                    {'name': 'readme.txt', 'path': 'templates/readme.txt', 'type': 'file'},
                    {'name': 'empty_subdir', 'path': 'templates/empty_subdir', 'type': 'dir'},
                ]
            elif path == 'templates/empty_subdir':
                return []  # Empty subdirectory
            return []
        
        service.fetch_directory_contents = mock_fetch
        
        result = service.fetch_directory_contents_recursive('owner', 'repo', 'main', 'templates')
        
        # Should have 2 files (empty subdir contributes nothing)
        assert len(result) == 2
        assert all(item['type'] == 'file' for item in result)
    
    def test_fetch_directory_contents_recursive_max_depth_protection(self):
        """Test recursive fetch stops at maximum depth to prevent excessive recursion."""
        service = GitHubSyncService()
        
        # Create a deeply nested structure that exceeds MAX_RECURSION_DEPTH
        def mock_fetch(owner, repo, branch, path):
            depth = path.count('/') + 1
            return [
                {'name': f'file_{depth}.md', 'path': f'{path}/file_{depth}.md', 'type': 'file'},
                {'name': f'level_{depth + 1}', 'path': f'{path}/level_{depth + 1}', 'type': 'dir'},
            ]
        
        service.fetch_directory_contents = mock_fetch
        
        result = service.fetch_directory_contents_recursive('owner', 'repo', 'main', 'level_0')
        
        # Should stop at MAX_RECURSION_DEPTH (10), so we get files from levels 0-9
        assert len(result) <= service.MAX_RECURSION_DEPTH
    
    def test_fetch_directory_contents_recursive_circular_reference_protection(self):
        """Test recursive fetch handles circular references (symlinks) gracefully."""
        service = GitHubSyncService()
        
        call_count = [0]  # Use list to allow modification in nested function
        
        def mock_fetch(owner, repo, branch, path):
            call_count[0] += 1
            if call_count[0] > 20:  # Safety limit for test
                return []
            if path == 'templates':
                return [
                    {'name': 'file1.md', 'path': 'templates/file1.md', 'type': 'file'},
                    {'name': 'subdir', 'path': 'templates/subdir', 'type': 'dir'},
                ]
            elif path == 'templates/subdir':
                return [
                    {'name': 'file2.md', 'path': 'templates/subdir/file2.md', 'type': 'file'},
                    # Simulate circular reference back to parent
                    {'name': 'link_to_templates', 'path': 'templates', 'type': 'dir'},
                ]
            return []
        
        service.fetch_directory_contents = mock_fetch
        
        result = service.fetch_directory_contents_recursive('owner', 'repo', 'main', 'templates')
        
        # Should complete without infinite loop
        assert len(result) == 2  # Only file1.md and file2.md
        file_paths = [f['path'] for f in result]
        assert 'templates/file1.md' in file_paths
        assert 'templates/subdir/file2.md' in file_paths


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


class TestLoadLocalTemplates:
    """Tests for load_local_templates.py script functionality."""
    
    def test_template_directories_constant_contains_both_directories(self):
        """Test that TEMPLATE_DIRECTORIES includes both agents and templates directories."""
        import sys
        import os
        
        # Add webapp to path to import the module
        webapp_path = os.path.join(os.path.dirname(__file__), '..')
        if webapp_path not in sys.path:
            sys.path.insert(0, webapp_path)
        
        # Import after path manipulation
        from load_local_templates import TEMPLATE_DIRECTORIES
        
        assert 'forge/templates/agents' in TEMPLATE_DIRECTORIES
        assert 'forge/templates/templates' in TEMPLATE_DIRECTORIES
        assert len(TEMPLATE_DIRECTORIES) == 2
    
    def test_template_directories_exist(self):
        """Test that all configured template directories exist on disk."""
        import os
        
        base_dir = os.path.join(os.path.dirname(__file__), '..')
        expected_dirs = [
            'forge/templates/agents',
            'forge/templates/templates',
        ]
        
        for template_dir in expected_dirs:
            full_path = os.path.join(base_dir, template_dir)
            assert os.path.exists(full_path), f"Template directory should exist: {full_path}"
            assert os.path.isdir(full_path), f"Should be a directory: {full_path}"
    
    def test_template_directories_contain_md_files(self):
        """Test that both template directories contain markdown files."""
        import os
        
        base_dir = os.path.join(os.path.dirname(__file__), '..')
        dirs_to_check = [
            ('forge/templates/agents', 10),  # Should have at least 10 agent prompts
            ('forge/templates/templates', 10),  # Should have at least 10 document templates
        ]
        
        for template_dir, min_count in dirs_to_check:
            full_path = os.path.join(base_dir, template_dir)
            md_files = [f for f in os.listdir(full_path) if f.endswith('.md')]
            assert len(md_files) >= min_count, \
                f"Directory {template_dir} should have at least {min_count} .md files, found {len(md_files)}"
