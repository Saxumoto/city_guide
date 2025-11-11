from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# Required to serve media files in development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Include Django's default authentication URLs (login, logout, etc.)
    # These views are named 'login', 'logout', 'password_change', etc., which fixes the NoReverseMatch error.
    path('accounts/', include('django.contrib.auth.urls')),

    # Redirect the base URL to the attraction list page
    path('', RedirectView.as_view(url='attractions/'), name='home'),

    # Include the URL patterns from our 'attractions' app
    path('attractions/', include('attractions.urls')),
]

# Only in development: serve media files from MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)