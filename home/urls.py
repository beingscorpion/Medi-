# from django.contrib import admin
# from django.urls import path,include
# from home import views

# urlpatterns = [
#     path('', views.index.as_view() , name="home"),
#     path('about', views.about.as_view() ,name="about" )
   

# ]

# urls.py - Main URL configuration

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Main pages
    path('', views.index.as_view(), name='index'),
    path('about/', views.about.as_view(), name='about'),
    path('features/', views.FeaturesView.as_view(), name='features'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Dashboard (requires authentication)
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Authentication URLs (Django's built-in auth views)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # API endpoints
    path('api/contact/', views.contact_form_api, name='api_contact'),
    path('api/newsletter/', views.newsletter_signup_api, name='api_newsletter'),
    
    # App-specific URLs (add your apps here)
    # path('exams/', include('apps.exams.urls')),
    # path('users/', include('apps.users.urls')),
    # path('certificates/', include('apps.certificates.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Add debug toolbar URLs if installed
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass