# portfolio/admin.py

from django.contrib import admin
from .models import Portfolio, Project

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Portfolio model.
    Displays user and portfolio title in the list view.
    Allows searching by user's username, name, and portfolio title.
    """
    list_display = ('user', 'portfolio_title')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'portfolio_title')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Project model.
    Displays project name, associated portfolio, and creation date in the list view.
    Allows filtering by creation/update dates and portfolio.
    Allows searching by project name and description.
    """
    list_display = ('project_name', 'portfolio', 'created_at')
    list_filter = ('created_at', 'updated_at', 'portfolio')
    search_fields = ('project_name', 'project_description')
