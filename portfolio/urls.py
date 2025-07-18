# portfolio/urls.py

from django.urls import path
from . import views # Import your views from the current app

urlpatterns = [
    # Route for the main dashboard (applicant list).
    # This will be accessible at the root of the included URL (e.g., / if included at '').
    path('', views.applicant_list_view, name='dashboard'),

    # Route for the detailed portfolio page of a specific user.
    # Uses the user's username as a URL parameter (e.g., /john_doe/).
    path('<str:username>/', views.PortfolioDetailView.as_view(), name='portfolio_detail'),

    # Route for the user deletion confirmation page.
    # Uses the user's username as a URL parameter (e.g., /delete/john_doe/).
    path('delete/<str:username>/', views.UserDeleteView.as_view(), name='user_delete'),
]
