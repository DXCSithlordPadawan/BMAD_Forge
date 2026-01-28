#!/usr/bin/env python
"""
Script to load templates from local directory into the database.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmad_forge.settings')
django.setup()

from forge.models import Template
from forge.services.template_parser import TemplateParser
from forge.services.github_sync import GitHubSyncService

def load_templates():
    """Load templates from the local templates directory."""
    templates_dir = os.path.join(os.path.dirname(__file__), 'forge', 'templates', 'agents')
    
    if not os.path.exists(templates_dir):
        print(f"Templates directory not found: {templates_dir}")
        return
    
    parser = TemplateParser()
    sync_service = GitHubSyncService()
    created_count = 0
    updated_count = 0
    
    # Process all .md files in the templates directory
    for filename in os.listdir(templates_dir):
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(templates_dir, filename)
        print(f"Processing: {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the template
            title = filename.replace('.md', '').replace('_', ' ').title()
            variables = parser.extract_variables_simple(content)
            description = sync_service.parse_template_description(content)
            agent_role = sync_service.detect_agent_role(content, filename)
            agent_roles = sync_service.detect_agent_roles(content, filename)
            workflow_phase = sync_service.detect_workflow_phase(content, filename)
            
            # Check if template already exists
            template, created = Template.objects.update_or_create(
                title=title,
                defaults={
                    'content': content,
                    'agent_role': agent_role,
                    'agent_roles': agent_roles,
                    'workflow_phase': workflow_phase,
                    'description': description or '',
                    'variables': variables,
                    'remote_path': filepath,
                    'is_active': True,
                }
            )
            
            roles_display = ', '.join(agent_roles)
            if created:
                created_count += 1
                print(f"  ✓ Created: {title} (roles: {roles_display})")
            else:
                updated_count += 1
                print(f"  ✓ Updated: {title} (roles: {roles_display})")
                
        except Exception as e:
            print(f"  ✗ Error processing {filename}: {e}")
    
    print(f"\n✓ Completed!")
    print(f"  Created: {created_count}")
    print(f"  Updated: {updated_count}")

if __name__ == '__main__':
    load_templates()
