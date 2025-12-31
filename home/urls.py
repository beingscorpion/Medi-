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
    path('', views.index, name='index'),
    path('contact', views.contact , name='contact' ),
    # path('login', views.login_view, name='login'),
    # path('register', views.register, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('chapter/<slug:slug>/', views.paper_selection_view, name='paper_selection'),
    path('mcq/<slug:slug>/<str:paper_type>/', views.mcq_view, name='mcq'),
    path('api/save-attempt/', views.save_attempt, name='save_attempt'),
    path('api/report-question/', views.report_question, name='report_question'),
    
    path('logout', views.logout_view, name='logout'),
    # path('login/', views.login.as_view(), name='login'),
    # path('login/', views.login_view, name='login')
    path('accounts/', include('allauth.urls')),
    # Dashboard (requires authentication)
    # path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
  
   