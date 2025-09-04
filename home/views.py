from django.shortcuts import render , HttpResponse
from home.models import Contact


# # Create your views here.
# def index(request):
#     # context ={
#     #     "check" : "hii"
#     # }

#     #  return render(request , "index.html" , context )
#     #  return HttpResponse("HELLO")
#     return render(request , "index.html")

# def about(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")  # Using form data, not a model class attribute
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")

#         new_contact = Contact( name=name, email=email, phone=phone, message=message )
#         new_contact.save()
        
#     return render(request , "about.html")
#     # return HttpResponse("about page pe aa gai")


# views.py - Example views for the homepage and other pages

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

class index(TemplateView):
    """
    Homepage view that renders the main landing page
    """
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Welcome to Docent',
            'meta_description': 'Transform your examination and certification processes with our comprehensive platform.',
            'features': [
                {
                    'title': 'Share your insights',
                    'description': 'Get detailed analytics and insights about candidate performance.',
                    'icon': 'chart-bar'
                },
                {
                    'title': 'Create new tests',
                    'description': 'Build comprehensive tests with our intuitive question builder.',
                    'icon': 'book-open'
                },
                {
                    'title': 'QA Office Setup',
                    'description': 'Establish quality assurance processes and maintain standards.',
                    'icon': 'check-circle'
                },
            ],
            'testimonials': [
                {
                    'name': 'Sarah Chen',
                    'position': 'Head of Training, TechCorp',
                    'content': 'Our certification processes have never been smoother.',
                    'avatar': 'https://images.unsplash.com/photo-1494790108755-2616b612b786'
                },
                {
                    'name': 'Michael Rodriguez', 
                    'position': 'Director of Learning, EduTech Solutions',
                    'content': 'The insights have helped us improve our course content significantly.',
                    'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d'
                }
            ]
        })
        return context

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    """
    Dashboard view for authenticated users
    """
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add dashboard-specific context here
        context.update({
            'active_exams': 24,
            'total_candidates': 156,
            'pass_rate': 89,
            'completed_exams': 42,
        })
        return context

class about(TemplateView):
    """
    About page view
    """
    template_name = 'pages/about.html'

class FeaturesView(TemplateView):
    """
    Features page view
    """
    template_name = 'pages/features.html'

class PricingView(TemplateView):
    """
    Pricing page view
    """
    template_name = 'pages/pricing.html'

class ContactView(TemplateView):
    """
    Contact page view
    """
    template_name = 'pages/contact.html'

# API Views
@require_http_methods(["POST"])
@csrf_exempt
def contact_form_api(request):
    """
    Handle contact form submissions via API
    """
    try:
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        # Validate required fields
        if not all([name, email, message]):
            return JsonResponse({
                'success': False,
                'message': 'All fields are required.'
            }, status=400)
        
        # Here you would typically:
        # 1. Save to database
        # 2. Send email notification
        # 3. Add to CRM system
        
        # For now, just return success
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your message. We\'ll get back to you soon!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }, status=500)

@require_http_methods(["POST"])
@csrf_exempt 
def newsletter_signup_api(request):
    """
    Handle newsletter signup via API
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email is required.'
            }, status=400)
        
        # Here you would typically:
        # 1. Validate email format
        # 2. Check if email already exists
        # 3. Add to newsletter service (Mailchimp, SendGrid, etc.)
        # 4. Send welcome email
        
        return JsonResponse({
            'success': True,
            'message': 'Successfully subscribed to newsletter!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }, status=500)