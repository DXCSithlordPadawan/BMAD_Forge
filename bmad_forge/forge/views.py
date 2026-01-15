"""
Views for BMAD Forge application.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.http import JsonResponse, FileResponse, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.db import models
from .models import Template, GeneratedPrompt
from .forms import DynamicPromptForm, TemplateFilterForm, GitHubSyncForm
from .services import GitHubSyncService, BMADValidator


class DashboardView(TemplateView):
    """
    Dashboard view showing template count and recent generated prompts.
    """
    
    template_name = 'forge/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_templates'] = Template.objects.filter(is_active=True).count()
        context['templates_by_role'] = self._get_templates_by_role()
        context['templates_by_phase'] = self._get_templates_by_phase()
        context['recent_prompts'] = GeneratedPrompt.objects.select_related('template')[:5]
        context['recent_templates'] = Template.objects.filter(is_active=True).order_by('-created_at')[:5]
        return context
    
    def _get_templates_by_role(self):
        """Get template counts grouped by agent role."""
        return dict(
            Template.objects.filter(is_active=True)
            .values('agent_role')
            .annotate(count=models.Count('id'))
            .values_list('agent_role', 'count')
        )
    
    def _get_templates_by_phase(self):
        """Get template counts grouped by workflow phase."""
        return dict(
            Template.objects.filter(is_active=True)
            .values('workflow_phase')
            .annotate(count=models.Count('id'))
            .values_list('workflow_phase', 'count')
        )


class TemplateListView(ListView):
    """
    List view for browsing and filtering templates.
    """
    
    model = Template
    template_name = 'forge/template_list.html'
    context_object_name = 'templates'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Template.objects.filter(is_active=True)
        
        # Apply filters
        agent_role = self.request.GET.get('agent_role')
        workflow_phase = self.request.GET.get('workflow_phase')
        search = self.request.GET.get('search')
        
        if agent_role:
            queryset = queryset.filter(agent_role=agent_role)
        if workflow_phase:
            queryset = queryset.filter(workflow_phase=workflow_phase)
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search) |
                models.Q(content__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TemplateFilterForm(self.request.GET)
        context['agent_roles'] = settings.BMAD_AGENT_ROLES
        context['workflow_phases'] = settings.BMAD_WORKFLOW_PHASES
        return context


class TemplateDetailView(DetailView):
    """
    Detail view showing template content and metadata.
    """
    
    model = Template
    template_name = 'forge/template_detail.html'
    context_object_name = 'template'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variables'] = self.object.get_variables_list()
        return context


class PromptFormView(FormView):
    """
    Form view for generating prompts from templates.
    """
    
    template_name = 'forge/prompt_form.html'
    
    def get_template(self):
        template_id = self.kwargs.get('template_id')
        return get_object_or_404(Template, id=template_id, is_active=True)
    
    def get_form(self, form_class=None):
        template = self.get_template()
        form = DynamicPromptForm(template=template, **self.get_form_kwargs())
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = self.get_template()
        return context
    
    def form_valid(self, form):
        template = self.get_template()
        
        # Generate the prompt
        final_output = form.generate_output()
        
        # Validate the generated prompt
        validation_report = BMADValidator.validate(final_output)
        
        # Create the GeneratedPrompt record
        generated_prompt = GeneratedPrompt.objects.create(
            template=template,
            input_data=form.cleaned_data,
            final_output=final_output,
            is_valid=validation_report['is_valid'],
            validation_notes=validation_report.get('notes', []),
            missing_variables=validation_report.get('unreplaced_variables', []),
        )
        
        # Add messages
        if validation_report['is_valid']:
            messages.success(self.request, 'Prompt generated successfully!')
        else:
            messages.warning(
                self.request,
                f'Prompt generated with {len(validation_report.get("issues", []))} issues'
            )
        
        return redirect('forge:prompt_result', pk=generated_prompt.id)


class PromptResultView(DetailView):
    """
    View for displaying generated prompt with validation results.
    """
    
    model = GeneratedPrompt
    template_name = 'forge/prompt_result.html'
    context_object_name = 'prompt'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validation_report'] = self.object.get_validation_status()
        
        # Get validation details
        validator_report = BMADValidator.validate(self.object.final_output)
        context['validation_details'] = validator_report
        
        return context


class PromptHistoryView(ListView):
    """
    View showing history of generated prompts.
    """
    
    model = GeneratedPrompt
    template_name = 'forge/prompt_history.html'
    context_object_name = 'prompts'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = GeneratedPrompt.objects.select_related('template')
        
        # Filter by validation status
        status = self.request.GET.get('status')
        if status == 'valid':
            queryset = queryset.filter(is_valid=True)
        elif status == 'invalid':
            queryset = queryset.filter(is_valid=False)
        
        return queryset


class GitHubSyncView(FormView):
    """
    View for GitHub synchronization interface.
    """
    
    template_name = 'forge/github_sync.html'
    form_class = GitHubSyncForm
    
    def get_initial(self):
        """Set initial values from settings."""
        return {
            'repo_url': f"https://github.com/{settings.TEMPLATE_REPO}",
            'path': 'aitrg/templates',
        }
    
    def form_valid(self, form):
        # Parse repository URL
        repo_url = form.cleaned_data['repo_url']
        path = form.cleaned_data['path']
        branch = form.cleaned_data.get('branch', 'main')
        
        # Extract owner and repo from URL
        parts = repo_url.rstrip('/').split('/')
        if len(parts) >= 2:
            owner = parts[-2]
            repo = parts[-1]
        else:
            messages.error(self.request, 'Invalid repository URL')
            return redirect('forge:github_sync')
        
        # Perform sync
        service = GitHubSyncService()
        results = service.sync_templates(owner, repo, branch, path)
        
        if results['success']:
            messages.success(
                self.request,
                f"Sync completed: {results['created']} created, {results['updated']} updated"
            )
        else:
            messages.error(self.request, f"Sync failed: {', '.join(results['errors'])}")
        
        return redirect('forge:template_list')


def manual_sync(request):
    """
    Manual sync endpoint using configured repository.
    """
    service = GitHubSyncService()
    results = service.sync_from_config()
    
    if results['success']:
        messages.success(
            request,
            f"Sync completed: {results['created']} created, {results['updated']} updated"
        )
    else:
        messages.error(request, f"Sync failed: {', '.join(results['errors'])}")
    
    return redirect('forge:template_list')


def download_prompt(request, pk):
    """
    Download generated prompt as a text file.
    """
    prompt = get_object_or_404(GeneratedPrompt, pk=pk)
    
    response = HttpResponse(
        prompt.final_output,
        content_type='text/plain; charset=utf-8'
    )
    filename = f"bmad_prompt_{pk}_{prompt.created_at.strftime('%Y%m%d_%H%M%S')}.txt"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def health_check(request):
    """
    Health check endpoint for monitoring.
    """
    return JsonResponse({
        'status': 'healthy',
        'app': settings.APP_NAME,
        'version': settings.APP_VERSION,
    })
