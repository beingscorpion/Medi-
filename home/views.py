from django.shortcuts import render , HttpResponse, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
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
from django.db.models import Count, Q
from home.models import Subject, Chapter, Question, UserQuestionAttempt, UserChapterStats , Contact, Province, PastPaperSubject, PastPaper
from django.http import FileResponse, Http404
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

@login_required
def dashboard_view(request):
    # Get the mode from request (default to 'mock-test')
    mode = request.GET.get('mode', 'mock-test')
    
    # Get user (or None if not authenticated)
    user = request.user if request.user.is_authenticated else None
    
    context = {
        'mode': mode,
        'user': user
    }
    
    if mode == 'past-paper':
        # Past Paper mode - show provinces and subjects
        provinces = Province.objects.all().order_by('name')
        subjects = PastPaperSubject.objects.all().order_by('name')
        
        # Prepare province data with subjects
        provinces_data = {}
        for province in provinces:
            # Get all subjects that have past papers for this province
            past_papers = PastPaper.objects.filter(province=province)
            subject_ids = past_papers.values_list('subject', flat=True).distinct()
            province_subjects = PastPaperSubject.objects.filter(ps_id__in=subject_ids)
            
            provinces_data[province.name] = {
                'province': province,
                'subjects': province_subjects
            }
        
        context.update({
            'provinces_data': provinces_data,
            'all_subjects': subjects
        })
    else:
        # Mock Test mode - original functionality
        # Get all subjects
        subjects = Subject.objects.all().order_by('name')
        
        # Prepare subject data with chapters and stats
        subjects_data = {}
        
        for subject in subjects:
            # Get all chapters for this subject
            chapters = Chapter.objects.filter(subject=subject).order_by('chapter_no')
            
            # Calculate subject-level stats
            total_questions = Question.objects.filter(chapter__subject=subject).count()
            
            if user:
                user_attempts = UserQuestionAttempt.objects.filter(
                    user=user,
                    question__chapter__subject=subject
                )
                completed = user_attempts.count()
                pending = total_questions - completed
            else:
                completed = 0
                pending = total_questions
            
            # Prepare chapter data with stats
            chapters_data = []
            for chapter in chapters:
                # Get or create user stats for this chapter
                if user:
                    stats, created = UserChapterStats.objects.get_or_create(
                        user=user,
                        chapter=chapter
                    )
                    # Always update stats to ensure they're current
                    stats.update_stats()
                    
                    chapter_stats = {
                        'total': stats.total_questions,
                        'completed': stats.attempted,
                        'pending': stats.pending,
                        'score': float(stats.score_percentage)
                    }
                else:
                    # For non-authenticated users, just show total questions
                    total_chapter_questions = chapter.questions.count()
                    chapter_stats = {
                        'total': total_chapter_questions,
                        'completed': 0,
                        'pending': total_chapter_questions,
                        'score': 0
                    }
                
                chapters_data.append({
                    'chapter': chapter,
                    'stats': chapter_stats
                })
            
            subjects_data[subject.name] = {
                'subject': subject,
                'chapters': chapters_data,
                'stats': {
                    'total': total_questions,
                    'completed': completed,
                    'pending': pending
                }
            }
        
        context['subjects_data'] = subjects_data
    
    return render(request, 'dashboard/dashboard.html', context)


def paper_selection_view(request, slug):
    """
    Paper type selection page - shows options for Past Papers, Subject Paper, Theory Paper
    """
    chapter = Chapter.objects.get(slug=slug)
    context = {
        'chapter_name': chapter.title,
        'chapter_description': chapter.description,
        'chapter_slug': chapter.slug,
    }

    return render(request, 'paper_selection.html', context)




def mcq_view(request, slug, paper_type):
    """
    MCQ page. Accepts chapter slug and paper type to load appropriate questions.
    Maps URL paper_type values to model paper_type choices.
    """
    # Map URL paper_type values to model paper_type choices
    paper_type_mapping = {
        'mcq': 'MCQ',
        'book-line-mcq': 'Book Line MCQ',
        'past-paper-mcq': 'Past Paper MCQ',
    }
    
    # Get the mapped paper_type, default to the original if not found
    mapped_paper_type = paper_type_mapping.get(paper_type.lower(), paper_type)
    
    # Filter questions by chapter slug and paper type
    questions = Question.objects.filter(chapter__slug=slug, paper_type=mapped_paper_type)
    
    # Get user attempts if authenticated
    user_attempts = {}
    if request.user.is_authenticated:
        attempts = UserQuestionAttempt.objects.filter(
            user=request.user,
            question__in=questions
        ).select_related('question')
        for attempt in attempts:
            user_attempts[attempt.question.q_id] = {
                'selected_text': attempt.selected_text,
                'is_correct': attempt.is_correct,
            }
    
    # Convert questions to JSON format for the template
    questions_data = []
    for q in questions:
        options = []
        if q.key1:
            options.append({'key': '1', 'label': q.key1})
        if q.key2:
            options.append({'key': '2', 'label': q.key2})
        if q.key3:
            options.append({'key': '3', 'label': q.key3})
        if q.key4:
            options.append({'key': '4', 'label': q.key4})
        
        # Determine correct answer key
        correct_key = None
        if q.correct_text:
            # Try to match correct_text with one of the keys
            if q.correct_text == q.key1:
                correct_key = '1'
            elif q.correct_text == q.key2:
                correct_key = '2'
            elif q.correct_text == q.key3:
                correct_key = '3'
            elif q.correct_text == q.key4:
                correct_key = '4'
            else:
                # If correct_text is a number (1-4), use it directly
                if q.correct_text.strip() in ['1', '2', '3', '4']:
                    correct_key = q.correct_text.strip()
        
        # Get user's previous attempt for this question
        attempt_data = user_attempts.get(q.q_id, {})
        
        questions_data.append({
            'id': q.q_id,
            'question': q.question,
            'options': options,
            'correct': correct_key,  # Default to '1' if not found
            'explanation': q.explanation or 'No explanation available.',
            'selected': attempt_data.get('selected_text', ''),
            'is_correct': attempt_data.get('is_correct', None),
        })
    
    context = {
        'questions_json': json.dumps(questions_data),
        'test_title': f'{mapped_paper_type} Practice',
        'questions': questions,  # Keep for backward compatibility if needed
        'user': request.user,
    }
    return render(request, 'mcq.html', context)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def save_attempt(request):
    """Save user's answer attempt to database"""
    try:
        question_id = request.POST.get('question_id')
        selected_text = request.POST.get('selected_text')
        
        if not question_id or not selected_text:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
        
        question = Question.objects.get(q_id=question_id)
        
        # Determine if answer is correct
        is_correct = False
        if question.correct_text:
            # Map correct_text to the actual option text
            key_map = {
                '1': question.key1,
                '2': question.key2,
                '3': question.key3,
                '4': question.key4,
            }
            
            # Check if correct_text is a key (1-4)
            if question.correct_text.strip() in ['1', '2', '3', '4']:
                correct_option_text = key_map.get(question.correct_text.strip())
                if selected_text == correct_option_text:
                    is_correct = True
            # Otherwise, check if correct_text directly matches selected_text
            elif selected_text == question.correct_text:
                is_correct = True
        
        # Get or create attempt
        attempt, created = UserQuestionAttempt.objects.get_or_create(
            user=request.user,
            question=question,
            defaults={
                'selected_text': selected_text,
                'is_correct': is_correct,
            }
        )
        
        if not created:
            # Update existing attempt
            attempt.selected_text = selected_text
            attempt.is_correct = is_correct
            attempt.save()
        
        # Update chapter stats after saving attempt
        chapter_stats, _ = UserChapterStats.objects.get_or_create(
            user=request.user,
            chapter=question.chapter
        )
        chapter_stats.update_stats()
        
        return JsonResponse({'success': True, 'is_correct': is_correct})
    except Question.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Question not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def report_question(request):
    """Report a question"""
    try:
        question_id = request.POST.get('question_id')
        
        if not question_id:
            return JsonResponse({'success': False, 'error': 'Missing question_id'}, status=400)
        
        question = Question.objects.get(q_id=question_id)
        question.report = True
        question.save()
        
        return JsonResponse({'success': True, 'message': 'Question reported successfully'})
    except Question.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Question not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# @csrf_exempt
# @require_http_methods(["POST"])
# def google_auth_view(request):
#     """
#     Handle Google Sign-In authentication
#     """
#     try:
#         data = json.loads(request.body)
#         credential = data.get('credential')
        
#         if not credential:
#             return JsonResponse({
#                 'success': False,
#                 'error': 'No credential provided'
#             }, status=400)
        
#         # Decode the JWT token
#         # For production, you should verify the token with Google's servers
#         try:
#             if JWT_AVAILABLE:
#                 # Use PyJWT if available
#                 decoded_token = jwt.decode(credential, options={"verify_signature": False})
#             else:
#                 # Manual JWT decoding (base64 decode the payload)
#                 parts = credential.split('.')
#                 if len(parts) != 3:
#                     raise ValueError("Invalid JWT format")
                
#                 # Decode the payload (second part)
#                 payload = parts[1]
#                 # Add padding if needed
#                 padding = 4 - len(payload) % 4
#                 if padding != 4:
#                     payload += '=' * padding
                
#                 # Decode base64
#                 decoded_bytes = base64.urlsafe_b64decode(payload)
#                 decoded_token = json.loads(decoded_bytes.decode('utf-8'))
            
#             email = decoded_token.get('email')
#             name = decoded_token.get('name', '')
#             given_name = decoded_token.get('given_name', '')
#             family_name = decoded_token.get('family_name', '')
#             google_id = decoded_token.get('sub')
#             picture = decoded_token.get('picture', '')
            
#             if not email:
#                 return JsonResponse({
#                     'success': False,
#                     'error': 'Email not found in token'
#                 }, status=400)
            
#             # Get or create user
#             user, created = User.objects.get_or_create(
#                 username=email,
#                 defaults={
#                     'email': email,
#                     'first_name': given_name,
#                     'last_name': family_name,
#                 }
#             )
            
#             # Update user info if it changed
#             if not created:
#                 user.email = email
#                 user.first_name = given_name
#                 user.last_name = family_name
#                 user.save()
            
#             # Log the user in
#             login(request, user)
            
#             return JsonResponse({
#                 'success': True,
#                 'redirect_url': '/dashboard/',
#                 'message': 'Successfully authenticated'
#             })
            
#         except (ValueError, json.JSONDecodeError, KeyError) as e:
#             return JsonResponse({
#                 'success': False,
#                 'error': f'Invalid token: {str(e)}'
#             }, status=400)
            
#     except json.JSONDecodeError:
#         return JsonResponse({
#             'success': False,
#             'error': 'Invalid JSON'
#         }, status=400)
#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'error': str(e)
#         }, status=500)

def logout_view(request):
    django_logout(request)
    return redirect('/')


# Past Paper Views
@login_required
def past_paper_years_view(request, province_id, subject_id):
    """
    Show years available for a specific province and subject combination
    """
    try:
        province = Province.objects.get(p_id=province_id)
        subject = PastPaperSubject.objects.get(ps_id=subject_id)
        
        # Get all past papers for this province and subject, ordered by year
        past_papers = PastPaper.objects.filter(
            province=province,
            subject=subject
        ).order_by('-year')
        
        # Get unique years with their corresponding past paper
        years_list = []
        seen_years = set()
        for past_paper in past_papers:
            if past_paper.year not in seen_years:
                years_list.append({
                    'year': past_paper.year,
                    'past_paper': past_paper
                })
                seen_years.add(past_paper.year)
        
        context = {
            'province': province,
            'subject': subject,
            'years_list': years_list
        }
        
        return render(request, 'past_paper_years.html', context)
    except (Province.DoesNotExist, PastPaperSubject.DoesNotExist):
        messages.error(request, 'Province or Subject not found')
        return redirect('dashboard')


@login_required
def download_past_paper(request, past_paper_id):
    """
    Download a past paper PDF
    """
    try:
        past_paper = PastPaper.objects.get(pp_id=past_paper_id)
        
        if past_paper.pdf_file and past_paper.pdf_file.name:
            try:
                file = past_paper.pdf_file.open('rb')
                response = FileResponse(
                    file,
                    content_type='application/pdf'
                )
                filename = f"{past_paper.province.name}_{past_paper.subject.name}_{past_paper.year}.pdf"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            except Exception as e:
                raise Http404(f"Error opening PDF file: {str(e)}")
        else:
            raise Http404("PDF file not found")
    except PastPaper.DoesNotExist:
        raise Http404("Past paper not found")




# def get_subject_stats(user, subject_name):
#     chapters = Chapter.objects.filter(subject__name=subject_name)
#     total_questions = Question.objects.filter(chapter__subject__name=subject_name).count()
    
#     user_attempts = UserQuestionAttempt.objects.filter(
#         user=user,
#         question__chapter__subject__name=subject_name
#     )
#     completed = user_attempts.count()
#     pending = total_questions - completed
    
#     return {
#         'total': total_questions,
#         'completed': completed,
#         'pending': pending
#     }


# def get_chapter_stats(user, chapter_slug):
#     chapter = Chapter.objects.get(slug=chapter_slug)
#     stats, created = UserChapterStats.objects.get_or_create(
#         user=user,
#         chapter=chapter
#     )
#     stats.update_stats()  # Recalculate
    
#     return {
#         'total': stats.total_questions,
#         'completed': stats.attempted,
#         'pending': stats.pending,
#         'score': stats.score_percentage
#     }










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
        