"""
URL patterns for BMAD Forge application.
"""

from django.urls import path
from . import views

app_name = 'forge'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Template URLs
    path('templates/', views.TemplateListView.as_view(), name='template_list'),
    path('templates/<int:pk>/', views.TemplateDetailView.as_view(), name='template_detail'),
    
    # Prompt URLs
    path('generate/<int:template_id>/', views.PromptFormView.as_view(), name='prompt_form'),
    path('prompts/<int:pk>/', views.PromptResultView.as_view(), name='prompt_result'),
    path('prompts/history/', views.PromptHistoryView.as_view(), name='prompt_history'),
    path('prompts/<int:pk>/download/', views.download_prompt, name='download_prompt'),
    
    # GitHub Sync URLs
    path('sync/', views.GitHubSyncView.as_view(), name='github_sync'),
    path('sync/manual/', views.manual_sync, name='manual_sync'),
]
