# portfolio/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.models import User # Import Django's built-in User model
from .models import Portfolio, Project # Import your custom models

@login_required # Ensures that only logged-in users can access this view
def applicant_list_view(request):
    """
    Function-based view to display a list of all applicants.
    An 'applicant' is defined as any Django User who has an associated Portfolio.
    This view serves as the main Job Applicant Dashboard.
    """
    # Retrieve all User objects that have an associated Portfolio.
    # .select_related('portfolio') optimizes the query by fetching related Portfolio data
    # in the same database hit, improving performance.
    # .order_by() sorts the applicants by first name, then last name.
    applicants = User.objects.filter(portfolio__isnull=False).select_related('portfolio').order_by('first_name', 'last_name')

    context = {
        'applicants': applicants,
        # The position is hardcoded as per the requirement.
        'position_applying_for': "Junior Developer",
    }
    # Renders the 'dashboard.html' template with the list of applicants and position info.
    return render(request, 'dashboard.html', context)

class PortfolioDetailView(LoginRequiredMixin, DetailView):
    """
    Class-based view to display the detailed portfolio of a specific user (applicant).
    The user is identified by their username, which is passed in the URL.
    """
    model = Portfolio # This view primarily operates on the Portfolio model
    template_name = 'portfolio_detail.html' # The template to render for this view
    context_object_name = 'portfolio' # The name of the context variable to use in the template

    def get_object(self, queryset=None):
        """
        Overrides the default get_object method to retrieve the Portfolio object
        based on the 'username' provided in the URL keyword arguments.
        """
        username = self.kwargs.get('username')
        if not username:
            # If no username is provided in the URL, raise a 404 error.
            raise Http404("Username not found in URL.")

        # Attempt to retrieve the User object based on the username.
        # get_object_or_404 will raise Http404 if the user does not exist.
        user = get_object_or_404(User, username=username)

        # Attempt to retrieve the Portfolio linked to this User.
        # If the Portfolio does not exist for the user, raise a 404 error.
        try:
            portfolio = user.portfolio
        except Portfolio.DoesNotExist:
            raise Http404(f"Portfolio does not exist for user '{username}'.")

        return portfolio

class UserDeleteView(LoginRequiredMixin, DeleteView):
    """
    Class-based view to handle the deletion of a User (who is an applicant).
    When a User is deleted, their associated Portfolio and Projects will also be
    automatically deleted due to the `on_delete=models.CASCADE` setting in the models.
    The user to be deleted is identified by their username in the URL.
    """
    model = User # This view operates on the User model directly
    template_name = 'user_confirm_delete.html' # Template for the deletion confirmation page
    success_url = reverse_lazy('dashboard') # URL to redirect to after successful deletion

    def get_object(self, queryset=None):
        """
        Overrides the default get_object method to retrieve the User object
        to be deleted based on the 'username' from the URL keyword arguments.
        """
        username = self.kwargs.get('username')
        if not username:
            # If no username is provided in the URL, raise a 404 error.
            raise Http404("Username not found in URL.")

        # Retrieve the User object to be deleted.
        user_to_delete = get_object_or_404(User, username=username)

        # Optional: Add a check here to prevent a user from deleting their own account
        # if user_to_delete == self.request.user:
        #     # You might want to redirect to an error page or show a message
        #     raise Http404("You cannot delete your own account through this interface.")

        return user_to_delete

    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed (i.e., the user confirmed deletion).
        It performs the actual deletion.
        """
        # The deletion of the Portfolio and Projects happens automatically
        # because of the CASCADE deletion defined in the Portfolio and Project models.
        return super().form_valid(form)
