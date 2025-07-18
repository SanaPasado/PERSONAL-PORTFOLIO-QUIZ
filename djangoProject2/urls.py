# myproject/urls.py

from django.contrib import admin
from django.urls import path, include # Ensure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls), # Django Admin URL
    # Include all URLs from the 'portfolio' app at the root path ('').
    # This means your dashboard will be at '/', portfolio details at '/<username>/', etc.
    path('', include('portfolio.urls')),
    # Removed: path('accounts/', include('django.contrib.auth.urls')),
    # Since you want to rely solely on the admin for login,
    # the default Django auth URLs are no longer included here.
    # Users will log in via the /admin/ URL.
]
