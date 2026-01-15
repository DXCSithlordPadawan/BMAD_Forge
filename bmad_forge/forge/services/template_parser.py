"""
Template parsing service for extracting variables and metadata.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TemplateVariable:
    """
    Represents a variable found in a template.
    """
    name: str
    syntax: str  # 'double_brace' or 'single_bracket'
    start_pos: int
    end_pos: int
    default_value: Optional[str] = None


class TemplateParser:
    """
    Service for parsing BMAD templates and extracting variables.
    """
    
    # Regex patterns for variable detection
    DOUBLE_BRACE_PATTERN = r'\{\{(\w+(?::[^}]+)?)\}\}'
    SINGLE_BRACKET_PATTERN = r'\[(\w+(?::[^\]]+)?)\]'
    
    # BMAD section patterns
    REQUIRED_SECTIONS = [
        '## Your Role',
        '## Input',
        '## Output Requirements',
    ]
    
    OPTIONAL_SECTIONS = [
        '## Context',
        '## Constraints',
        '## Examples',
        '## Step-by-Step Instructions',
        '## Success Criteria',
        '## Notes',
    ]
    
    ALL_SECTIONS = REQUIRED_SECTIONS + OPTIONAL_SECTIONS
    
    @classmethod
    def extract_variables(cls, content: str) -> List[TemplateVariable]:
        """
        Extract all variables from template content.
        
        Args:
            content: Template content string
            
        Returns:
            List of TemplateVariable objects
        """
        variables = []
        
        # Find double brace variables: {{VAR_NAME}} or {{VAR_NAME:default}}
        for match in re.finditer(cls.DOUBLE_BRACE_PATTERN, content):
            var = TemplateVariable(
                name=match.group(1).split(':')[0],
                syntax='double_brace',
                start_pos=match.start(),
                end_pos=match.end(),
                default_value=match.group(1).split(':')[1] if ':' in match.group(1) else None
            )
            if var not in variables:
                variables.append(var)
        
        # Find single bracket variables: [VAR_NAME]
        for match in re.finditer(cls.SINGLE_BRACKET_PATTERN, content):
            var = TemplateVariable(
                name=match.group(1),
                syntax='single_bracket',
                start_pos=match.start(),
                end_pos=match.end(),
            )
            if var not in variables:
                variables.append(var)
        
        return variables
    
    @classmethod
    def extract_variables_simple(cls, content: str) -> List[str]:
        """
        Extract variable names from template content (simple version).
        
        Args:
            content: Template content string
            
        Returns:
            List of variable names
        """
        pattern = r'\{\{(\w+)\}\}|\[(\w+)\]'
        matches = re.findall(pattern, content)
        variables = set()
        for match in matches:
            variables.add(match[0] if match[0] else match[1])
        return sorted(list(variables))
    
    @classmethod
    def detect_sections(cls, content: str) -> Dict[str, Tuple[int, int]]:
        """
        Detect BMAD sections in template content.
        
        Args:
            content: Template content string
            
        Returns:
            Dictionary mapping section names to their (start, end) positions
        """
        sections = {}
        content_lower = content.lower()
        
        for section in cls.ALL_SECTIONS:
            section_lower = section.lower()
            pos = content_lower.find(section_lower)
            if pos != -1:
                sections[section] = (pos, pos + len(section))
        
        return sections
    
    @classmethod
    def check_required_sections(cls, content: str) -> Tuple[bool, List[str]]:
        """
        Check if all required BMAD sections are present.
        
        Args:
            content: Template content string
            
        Returns:
            Tuple of (is_valid, list of missing sections)
        """
        sections = cls.detect_sections(content)
        missing = []
        
        for section in cls.REQUIRED_SECTIONS:
            if section not in sections:
                missing.append(section)
        
        return len(missing) == 0, missing
    
    @classmethod
    def validate_template(cls, content: str) -> Dict:
        """
        Validate a template for BMAD compliance.
        
        Args:
            content: Template content string
            
        Returns:
            Dictionary with validation results
        """
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'variables': [],
            'sections': [],
        }
        
        # Check required sections
        is_valid, missing = cls.check_required_sections(content)
        if not is_valid:
            result['is_valid'] = False
            result['errors'].append(f"Missing required sections: {', '.join(missing)}")
        
        # Extract variables
        variables = cls.extract_variables(content)
        result['variables'] = [
            {
                'name': v.name,
                'syntax': v.syntax,
                'has_default': v.default_value is not None,
            }
            for v in variables
        ]
        
        # Check for potential issues
        if not variables:
            result['warnings'].append("No variables found in template")
        
        # Detect present sections
        sections = cls.detect_sections(content)
        result['sections'] = list(sections.keys())
        
        return result
    
    @classmethod
    def substitute_variables(cls, content: str, values: Dict[str, str]) -> str:
        """
        Substitute variables in template content with provided values.
        
        Args:
            content: Template content string
            values: Dictionary mapping variable names to replacement values
            
        Returns:
            Content with variables substituted
        """
        result = content
        
        for var_name, value in values.items():
            # Replace double brace syntax
            result = result.replace('{{' + var_name + '}}', str(value))
            # Replace single bracket syntax
            result = result.replace('[' + var_name + ']', str(value))
        
        return result
    
    @classmethod
    def find_unreplaced_variables(cls, content: str) -> List[str]:
        """
        Find variables that were not replaced (still present in content).
        
        Args:
            content: Template content string
            
        Returns:
            List of unreplaced variable names
        """
        variables = cls.extract_variables_simple(content)
        # Check if any variables remain in content
        unreplaced = []
        for var in variables:
            if '{{' + var + '}}' in content or '[' + var + ']' in content:
                unreplaced.append(var)
        return unreplaced
