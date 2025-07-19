# portfolio/models.py

from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    """
    Represents a user's portfolio, with a one-to-one link to a Django User.
    When a User is deleted, their associated Portfolio will also be deleted.
    """
    # One-to-one relationship with the User model.
    # on_delete=models.CASCADE ensures that if a User is deleted,
    # their corresponding Portfolio is also deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    portfolio_title = models.CharField(max_length=200)
    portfolio_description = models.TextField(blank=True, null=True)

    class Meta:
        # Proper plural name for the Django Admin interface
        verbose_name_plural = "Portfolios"

    def __str__(self):
        """
        Returns a string representation of the Portfolio object,
        displaying "User First Name - Portfolio" in the Django Admin.
        """
        return f"{self.user.first_name} - Portfolio"

class Project(models.Model):
    """
    Represents a project within a user's portfolio.
    A single Project can only be assigned to a single Portfolio.
    """
    # Foreign key to the Portfolio model.
    # on_delete=models.CASCADE ensures that if a Portfolio is deleted,
    # all its associated Projects are also deleted.
    # related_name='projects' allows accessing projects from a portfolio instance: portfolio.projects.all()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=200)
    project_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Automatically sets the creation timestamp
    updated_at = models.DateTimeField(auto_now=True)     # Automatically updates the timestamp on each save

    class Meta:
        # Order projects by creation date, newest first
        ordering = ['-created_at']
        # Proper plural name for the Django Admin interface
        verbose_name_plural = "Projects"

    def __str__(self):
        """
        Returns a string representation of the Project object,
        displaying only the project_name in the Django Admin.
        """
        return self.project_name
