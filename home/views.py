from django.shortcuts import render , HttpResponse, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from home.models import Contact
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
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

# def login_view(request):
#     if request.method == 'POST':
#         identifier = request.POST.get('email')
#         password = request.POST.get('password')
#         user = None
#         if identifier:
#             # if '@' in identifier:
#             try:
#                 existing_user = User.objects.get(email=identifier)
#                 user = authenticate(request, username=existing_user.username, password=password)
#             except User.DoesNotExist:
#                 user = None
#             # else:
#             #     user = authenticate(request, username=identifier, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/dashboard/')
#         else:
#             messages.error(request, 'Invalid email or password')
#             return redirect('/')
#     return redirect('/')

# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         if not all([username, email, password]):
#             messages.error(request, 'All fields are required')
#             # return redirect('/')

#         # Prevent duplicate usernames (case-insensitive)
#         if User.objects.filter(username__iexact=username).exists():
#             messages.error(request, 'Username is already taken')
#             # return redirect('/')

#         # Prevent duplicate emails (case-insensitive)
#         if User.objects.filter(email__iexact=email).exists():
#             messages.error(request, 'Email is already registered')
#             # return redirect('/')

#         try:
#             user = User.objects.create_user(username=username, email=email, password=password)
#         except Exception:
#             messages.error(request, 'Could not create account. Username or email may already exist.')
#             # return redirect('/')

#         login(request, user)
#         return redirect('/dashboard/')
#     return redirect('/')

# @login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


def paper_selection_view(request, slug=None):
    """
    Paper type selection page - shows options for Past Papers, Subject Paper, Theory Paper
    """
    # Map chapter slugs to display names
    chapter_names = {
        'cell-biology': 'Cell Biology',
        'genetics': 'Genetics',
        'ecology': 'Ecology',
        'organic-chemistry': 'Organic Chemistry',
        'inorganic-chemistry': 'Inorganic Chemistry',
        'physical-chemistry': 'Physical Chemistry',
        'mechanics': 'Mechanics',
        'thermodynamics': 'Thermodynamics',
        'optics': 'Optics',
        'grammar': 'Grammar',
        'vocabulary': 'Vocabulary',
        'comprehension': 'Comprehension',
    }
    
    chapter_descriptions = {
        'cell-biology': 'Cell Structure, Organelles, Functions',
        'genetics': 'DNA, RNA, Inheritance Patterns',
        'ecology': 'Ecosystems, Food Chains, Biomes',
        'organic-chemistry': 'Hydrocarbons, Functional Groups, Reactions',
        'inorganic-chemistry': 'Elements, Compounds, Periodic Table',
        'physical-chemistry': 'Thermodynamics, Kinetics, Equilibrium',
        'mechanics': 'Motion, Forces, Energy, Momentum',
        'thermodynamics': 'Heat, Temperature, Entropy',
        'optics': 'Light, Reflection, Refraction, Lenses',
        'grammar': 'Tenses, Parts of Speech, Syntax',
        'vocabulary': 'Word Meanings, Synonyms, Antonyms',
        'comprehension': 'Reading, Analysis, Interpretation',
    }
    
    context = {
        'chapter_slug': slug or 'chapter',
        'chapter_name': chapter_names.get(slug, 'Chapter'),
        'chapter_description': chapter_descriptions.get(slug, 'Select a paper type to start practicing'),
    }
    
    return render(request, 'paper_selection.html', context)


def mcq_view(request, slug=None, paper_type=None):
    """
    MCQ page. Accepts chapter slug and paper type to load appropriate questions.
    """
    # TODO: replace this mock data with DB-backed questions filtered by slug/chapter
    questions = [
        {
            "id": 1,
            "question": "Which planet in our Solar System is known as the 'Red Planet' due to its reddish appearance?",
            "options": [
                {"key": "A", "label": "A. Jupiter"},
                {"key": "B", "label": "B. Mars"},
                {"key": "C", "label": "C. Venus"},
                {"key": "D", "label": "D. Saturn"},
            ],
            "correct": "B",
            "explanation": "Mars looks red because of iron oxide (rust) on its surface.",
        },
        {
            "id": 2,
            "question": "What gas do plants primarily absorb for photosynthesis?",
            "options": [
                {"key": "A", "label": "A. Oxygen"},
                {"key": "B", "label": "B. Nitrogen"},
                {"key": "C", "label": "C. Carbon Dioxide"},
                {"key": "D", "label": "D. Hydrogen"},
            ],
            "correct": "C",
            "explanation": "Plants absorb carbon dioxide and release oxygen during photosynthesis.",
        },
        {
            "id": 3,
            "question": "For the quadratic function $f(x) = e^{x^2} - \\varepsilon x + \\dfrac{3}{x}$ with $\\varepsilon > 0$, which statement is true about its behavior as $x \\to +\\infty$?",
            "options": [
                {"key": "A", "label": "A. $f(x)$ is dominated by $\\dfrac{3}{x}$ so $f(x) \\to 0$"},
                {"key": "B", "label": "B. $f(x)$ grows like $-\\varepsilon x$ so $f(x) \\to -\\infty$"},
                {"key": "C", "label": "C. $f(x)$ grows like $e^{x^2}$ so $f(x) \\to +\\infty$"},
                {"key": "D", "label": "D. $f(x)$ oscillates because of the fraction term"},
            ],
            "correct": "C",
            "explanation": "As $x \\to +\\infty$, the dominant term is $e^{x^2}$, which outgrows both the linear term $\\varepsilon x$ and the fractional term $\\dfrac{3}{x}$, so $f(x) \\to +\\infty$.",
        },
    ]

    # Map paper types to test titles
    paper_titles = {
        'past-papers': 'Past Papers',
        'subject-paper': 'Subject Paper',
        'theory-paper': 'Theory Paper',
    }
    
    # Build test title
    chapter_name = slug.replace('-', ' ').title() if slug else 'Chapter'
    paper_name = paper_titles.get(paper_type, 'Practice Test')
    test_title = f"{paper_name} - {chapter_name}"
    
    context = {
        "slug": slug,
        "paper_type": paper_type,
        "questions_json": json.dumps(questions),
        "test_title": test_title,
    }
    return render(request, 'mcq.html', context)

# def logout_view(request):
#     django_logout(request)
#     return redirect('/')















###--------------------------------------------------------------------------------------
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
        