"""
Tests for BMAD Forge views.
"""

import pytest
from django.urls import reverse
from forge.models import Template, GeneratedPrompt


@pytest.mark.django_db
class TestDashboardView:
    """Tests for the dashboard view."""
    
    def test_dashboard_view(self, client):
        """Test dashboard loads correctly."""
        response = client.get(reverse('forge:dashboard'))
        
        assert response.status_code == 200
        assert 'BMAD Forge' in response.content.decode()
    
    def test_dashboard_shows_template_count(self, client):
        """Test dashboard displays template count."""
        Template.objects.create(
            title='Test Template',
            content='test',
            agent_role='developer',
            workflow_phase='development',
        )
        
        response = client.get(reverse('forge:dashboard'))
        
        content = response.content.decode()
        assert '1' in content or 'Total Templates' in content


@pytest.mark.django_db
class TestTemplateListView:
    """Tests for the template list view."""
    
    def test_template_list(self, client):
        """Test template list loads."""
        response = client.get(reverse('forge:template_list'))
        
        assert response.status_code == 200
    
    def test_template_list_with_templates(self, client):
        """Test template list shows templates."""
        Template.objects.create(
            title='Developer Template',
            content='test',
            agent_role='developer',
            workflow_phase='development',
        )
        Template.objects.create(
            title='Analyst Template',
            content='test',
            agent_role='analyst',
            workflow_phase='planning',
        )
        
        response = client.get(reverse('forge:template_list'))
        content = response.content.decode()
        
        assert 'Developer Template' in content
        assert 'Analyst Template' in content
    
    def test_template_filter_by_role(self, client):
        """Test filtering templates by agent role."""
        Template.objects.create(
            title='Dev Template',
            content='test',
            agent_role='developer',
            workflow_phase='development',
        )
        Template.objects.create(
            title='Analyst Template',
            content='test',
            agent_role='analyst',
            workflow_phase='planning',
        )
        
        response = client.get(reverse('forge:template_list') + '?agent_role=developer')
        content = response.content.decode()
        
        assert 'Dev Template' in content
        assert 'Analyst Template' not in content
    
    def test_template_search(self, client):
        """Test searching templates."""
        Template.objects.create(
            title='Authentication Template',
            content='test',
            agent_role='developer',
            workflow_phase='development',
        )
        
        response = client.get(reverse('forge:template_list') + '?search=auth')
        content = response.content.decode()
        
        assert 'Authentication Template' in content


@pytest.mark.django_db
class TestPromptFormView:
    """Tests for the prompt generation form view."""
    
    def test_prompt_form_loads(self, client):
        """Test prompt form loads correctly."""
        template = Template.objects.create(
            title='Test Template',
            content='Hello {{name}}!',
            agent_role='developer',
            workflow_phase='development',
        )
        
        response = client.get(reverse('forge:prompt_form', args=[template.id]))
        
        assert response.status_code == 200
    
    def test_prompt_form_generates_prompt(self, client):
        """Test form submission generates a prompt."""
        template = Template.objects.create(
            title='Test Template',
            content='Hello {{name}}!',
            agent_role='developer',
            workflow_phase='development',
        )
        
        response = client.post(
            reverse('forge:prompt_form', args=[template.id]),
            {'name': 'World'}
        )
        
        assert response.status_code == 302
        assert GeneratedPrompt.objects.filter(template=template).exists()


@pytest.mark.django_db
class TestPromptResultView:
    """Tests for the prompt result view."""
    
    def test_prompt_result_view(self, client):
        """Test viewing a generated prompt."""
        template = Template.objects.create(
            title='Test',
            content='Hello {{name}}!',
            agent_role='developer',
            workflow_phase='development',
        )
        prompt = GeneratedPrompt.objects.create(
            template=template,
            input_data={'name': 'World'},
            final_output='Hello World!',
            is_valid=True,
        )
        
        response = client.get(reverse('forge:prompt_result', args=[prompt.id]))
        
        assert response.status_code == 200
        assert 'Hello World!' in response.content.decode()
    
    def test_prompt_result_shows_validation(self, client):
        """Test validation status is displayed."""
        template = Template.objects.create(
            title='Test',
            content='test',
            agent_role='developer',
            workflow_phase='development',
        )
        prompt = GeneratedPrompt.objects.create(
            template=template,
            input_data={},
            final_output='test',
            is_valid=False,
            validation_notes=['Missing section'],
        )
        
        response = client.get(reverse('forge:prompt_result', args=[prompt.id]))
        content = response.content.decode()
        
        assert 'Invalid' in content or 'Needs Review' in content


@pytest.mark.django_db
class TestGitHubSyncView:
    """Tests for the GitHub sync view."""
    
    def test_sync_view_loads(self, client):
        """Test sync view loads."""
        response = client.get(reverse('forge:github_sync'))
        
        assert response.status_code == 200
        assert 'GitHub' in response.content.decode() or 'Sync' in response.content.decode()


@pytest.mark.django_db
class TestPromptHistoryView:
    """Tests for the prompt history view."""
    
    def test_history_view_loads(self, client):
        """Test history view loads."""
        response = client.get(reverse('forge:prompt_history'))
        
        assert response.status_code == 200
    
    def test_history_shows_prompts(self, client):
        """Test history displays generated prompts."""
        template = Template.objects.create(
            title='Test',
            content='test',
            agent_role='developer',
            workflow_phase='development',
        )
        GeneratedPrompt.objects.create(
            template=template,
            input_data={},
            final_output='test',
            is_valid=True,
        )
        
        response = client.get(reverse('forge:prompt_history'))
        content = response.content.decode()
        
        assert 'Test' in content
