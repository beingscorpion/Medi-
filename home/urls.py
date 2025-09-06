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

    # Popup Login
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Google OAuth (django-allauth)
    path('accounts/', include('allauth.urls')),

    # API endpoints
    path('api/contact/', views.contact_form_api, name='api_contact'),
    path('api/newsletter/', views.newsletter_signup_api, name='api_newsletter'),
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