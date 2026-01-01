from django.shortcuts import redirect
from django.urls import reverse

class AdminAccessMiddleware:
    """
    Middleware jo check karta hai ke user staff ya superuser hai.
    Agar nahi hai to home page par redirect kar deta hai.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check karein ke path /admin/ se start hota hai
        if request.path.startswith('/admin/'):
            # Agar user authenticated nahi hai
            if not request.user.is_authenticated:
                return redirect('/')  # Home page par redirect
            
            # Agar user staff ya superuser nahi hai
            if not (request.user.is_staff or request.user.is_superuser):
                return redirect('/')  # Home page par redirect
        
        response = self.get_response(request)
        return response