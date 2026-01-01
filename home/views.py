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
from home.models import Subject, Chapter, Question, UserQuestionAttempt, UserChapterStats, Contact, Province, PastPaperYear, PastPaperQuestion, UserPastPaperAttempt
import json
from django.contrib.admin.views.decorators import staff_member_required 


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
    # chapters = Chapter.objects.filter(subject__name=subject_name)
    # total_questions = Question.objects.filter(chapter__subject__name=subject_name).count()
    
    # user_attempts = UserQuestionAttempt.objects.filter(
    #     user=user,
    #     question__chapter__subject__name=subject_name
    # )
    # completed = user_attempts.count()
    # pending = total_questions - completed

    
    
    # Get user (or None if not authenticated)
    user = request.user if request.user.is_authenticated else None
    
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
    
    # Get all provinces for Past Papers
    provinces = Province.objects.all().order_by('name')
    
    # Prepare province data with years and stats
    provinces_data = {}
    
    for province in provinces:
        # Get all years for this province
        years = PastPaperYear.objects.filter(province=province).order_by('-year')
        
        # Calculate province-level stats
        total_questions = PastPaperQuestion.objects.filter(year__province=province).count()
        
        if user:
            user_attempts = UserPastPaperAttempt.objects.filter(
                user=user,
                question__year__province=province
            )
            completed = user_attempts.count()
            pending = total_questions - completed
        else:
            completed = 0
            pending = total_questions
        
        # Prepare year data with stats
        years_data = []
        for year in years:
            # Calculate year-level stats
            total_year_questions = year.questions.count()
            
            if user:
                year_attempts = UserPastPaperAttempt.objects.filter(
                    user=user,
                    question__year=year
                )
                year_completed = year_attempts.count()
                year_correct = year_attempts.filter(is_correct=True).count()
                year_score = (year_correct / year_completed * 100) if year_completed > 0 else 0
            else:
                year_completed = 0
                year_score = 0
            
            years_data.append({
                'year': year,
                'stats': {
                    'total': total_year_questions,
                    'completed': year_completed,
                    'pending': total_year_questions - year_completed,
                    'score': float(year_score)
                }
            })
        
        provinces_data[province.name] = {
            'province': province,
            'years': years_data,
            'stats': {
                'total': total_questions,
                'completed': completed,
                'pending': pending
            }
        }
    
    context = {
        'subjects_data': subjects_data,
        'provinces_data': provinces_data,
        'user': user
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def paper_selection_view(request, slug):
    """
    Paper type selection page - shows options for Past Papers, Subject Paper, Theory Paper
    """
    chapter = Chapter.objects.get(slug=slug)
    user = request.user if request.user.is_authenticated else None
    
    # Paper types mapping - using template-friendly keys
    paper_types = [
        {'key': 'mcq', 'url': 'mcq', 'db_type': 'MCQ', 'title': 'MCQ'},
        {'key': 'book_line_mcq', 'url': 'book-line-mcq', 'db_type': 'Book Line MCQ', 'title': 'Book Line MCQ'},
        {'key': 'past_paper_mcq', 'url': 'past-paper-mcq', 'db_type': 'Past Paper MCQ', 'title': 'Past Paper MCQ'},
    ]
    
    # Calculate stats for each paper type
    paper_stats = {}
    for paper_info in paper_types:
        questions = Question.objects.filter(chapter=chapter, paper_type=paper_info['db_type'])
        total = questions.count()
        
        if user:
            attempts = UserQuestionAttempt.objects.filter(
                user=user,
                question__in=questions
            )
            completed = attempts.count()
            correct = attempts.filter(is_correct=True).count()
            pending = total - completed
            score = (correct / completed * 100) if completed > 0 else 0
        else:
            completed = 0
            correct = 0
            pending = total
            score = 0
        
        paper_stats[paper_info['key']] = {
            'total': total,
            'completed': completed,
            'pending': pending,
            'correct': correct,
            'score': float(score),
            'url': paper_info['url'],
            'title': paper_info['title'],
        }
    
    context = {
        'chapter_name': chapter.title,
        'chapter_description': chapter.description,
        'chapter_slug': chapter.slug,
        'paper_stats': paper_stats,
        'user': user,
    }

    return render(request, 'paper_selection.html', context)




@login_required
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
        'is_past_paper': False,  # Flag to indicate this is not a past paper
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

@login_required
def past_paper_mcq_view(request, slug):
    """
    Past Paper MCQ page. Accepts year slug to load appropriate questions.
    """
    # Get the year by slug
    try:
        year = PastPaperYear.objects.get(slug=slug)
    except PastPaperYear.DoesNotExist:
        return HttpResponse("Year not found", status=404)
    
    # Filter questions by year
    questions = PastPaperQuestion.objects.filter(year=year)
    
    # Get user attempts if authenticated
    user_attempts = {}
    if request.user.is_authenticated:
        attempts = UserPastPaperAttempt.objects.filter(
            user=request.user,
            question__in=questions
        ).select_related('question')
        for attempt in attempts:
            user_attempts[attempt.question.ppq_id] = {
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
        attempt_data = user_attempts.get(q.ppq_id, {})
        
        questions_data.append({
            'id': q.ppq_id,
            'question': q.question,
            'options': options,
            'correct': correct_key,
            'explanation': q.explanation or 'No explanation available.',
            'selected': attempt_data.get('selected_text', ''),
            'is_correct': attempt_data.get('is_correct', None),
        })
    
    context = {
        'questions_json': json.dumps(questions_data),
        'test_title': f'{year.province.name} {year.year} Past Paper',
        'questions': questions,
        'user': request.user,
        'is_past_paper': True,  # Flag to indicate this is a past paper
    }
    return render(request, 'mcq.html', context)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def save_past_paper_attempt(request):
    """Save user's past paper answer attempt to database"""
    try:
        question_id = request.POST.get('question_id')
        selected_text = request.POST.get('selected_text')
        
        if not question_id or not selected_text:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
        
        question = PastPaperQuestion.objects.get(ppq_id=question_id)
        
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
        attempt, created = UserPastPaperAttempt.objects.get_or_create(
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
        
        return JsonResponse({'success': True, 'is_correct': is_correct})
    except PastPaperQuestion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Question not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def logout_view(request):
    django_logout(request)
    return redirect('/')


def socialaccount_login_cancelled(request):
    return redirect('/')




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
        