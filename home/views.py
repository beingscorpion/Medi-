from django.shortcuts import render , HttpResponse
from home.models import Contact
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Create your views here.
def index(request):
    # context ={
    #     "check" : "hii"
    # }

    #  return render(request , "index.html" , context )
    #  return HttpResponse("HELLO")
    return render(request , "index.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")  # Using form data, not a model class attribute
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        new_contact = Contact( name=name, email=email, phone=phone, message=message )
        new_contact.save()
        
    return render(request , "contact.html")
    # return HttpResponse("about page pe aa gai")


# views.py - Example views for the homepage and other pages



# class index(TemplateView):
#     # """
#     # Homepage view that renders the main landing page
#     # """
#     template_name = 'index.html'
    
    
    #     return context

# @method_decorator(login_required, name='dispatch')
# class DashboardView(TemplateView):
#     """
#     Dashboard view for authenticated users
#     """
#     template_name = 'dashboard/dashboard.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Add dashboard-specific context here
#         context.update({
#             'active_exams': 24,
#             'total_candidates': 156,
#             'pass_rate': 89,
#             'completed_exams': 42,
#         })
#         return context


# class login(TemplateView):
#     """
#     Login page view
#     """
#     template_name = 'components/login_model.html'



# # API Views
# @require_http_methods(["POST"])
# @csrf_exempt
# def contact_form_api(request):
#     """
#     Handle contact form submissions via API
#     """
#     try:
#         data = json.loads(request.body)
#         name = data.get('name')
#         email = data.get('email')
#         message = data.get('message')
        
#         # Validate required fields
#         if not all([name, email, message]):
#             return JsonResponse({
#                 'success': False,
#                 'message': 'All fields are required.'
#             }, status=400)
        
#         # Here you would typically:
#         # 1. Save to database
#         # 2. Send email notification
#         # 3. Add to CRM system
        
#         # For now, just return success
        