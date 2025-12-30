from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# from phonenumber_field.phonenumber import PhoneNumber
# from phonenumber_field.validators import validate_international_phonenumber

# phone = PhoneNumber.from_string(phone_number='03001234567', region='PK')
# print(phone.is_valid())  # True
# print(str(phone)) 

# Create your models here.

class Contact (models.Model):
    # user = models.ForeignKey(User, on_delete=models.SET_NULL , null= True, blank=True)
    name = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    message = models.TextField()

    

    # class Meta:
    #     verbose_name = _("")
    #     verbose_name_plural = _("s")
    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk}


# class AcellularLife(models.Model):
#     PAPER_CHOICES = [
#         ('MCQ', 'MCQ'),
#         ('Descriptive', 'Descriptive'),
#         # add more types if needed
#     ]

#     REPORT_CHOICES = [
#         ('Yes', 'Yes'),
#         ('No', 'No'),
#     ]

#     q_id = models.AutoField(primary_key=True)
#     paper_type = models.CharField(max_length=50, choices=PAPER_CHOICES)
#     question = models.TextField()
#     key1 = models.CharField(max_length=255)
#     key2 = models.CharField(max_length=255)
#     key3 = models.CharField(max_length=255)
#     key4 = models.CharField(max_length=255)
#     correct_key = models.CharField(max_length=255)
#     explanation = models.TextField(blank=True, null=True)
#     report = models.CharField(max_length=3, choices=REPORT_CHOICES, default='No')

#     def __str__(self):
#         return f"{self.q_id} - {self.question[:50]}"
    
#     class Meta:
#         verbose_name = 'Acellular Life'

class Subject(models.Model):
    s_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Chapter(models.Model):
    c_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    chapter_no = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)  # For URLs like 'cell-biology'
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('subject', 'chapter_no')
        ordering = ['subject', 'chapter_no']
    
    def __str__(self):
        return f"{self.subject.name} - {self.title}"

class Question(models.Model):
    q_id = models.AutoField(primary_key=True)
    QUESTION_TYPES = (
        ('MCQ', 'MCQ'),
        ('Book Line MCQ', 'Book Line MCQ'),
        ('Past Paper MCQ', 'Past Paper MCQ'),
    )
    
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='questions')
    paper_type = models.CharField(max_length=50, choices=QUESTION_TYPES)  # Past Papers, Subject Paper, Theory Paper
    question = models.TextField()
    
    # MCQ options
    key1 = models.CharField(max_length=255, blank=True, null=True)
    key2 = models.CharField(max_length=255, blank=True, null=True)
    key3 = models.CharField(max_length=255, blank=True, null=True)
    key4 = models.CharField(max_length=255, blank=True, null=True)
    
    # Correct answer (1-4 for MCQ, 1=True/2=False for TF, text for FIB)
    correct_text = models.CharField(max_length=255, blank=True, null=True)
    
    explanation = models.TextField(blank=True)
    report = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['chapter', 'paper_type']),
        ]
    
    def __str__(self):
        return f"{self.chapter.title} - Q{self.q_id}"



class UserQuestionAttempt(models.Model):
    uq_id = models.AutoField(primary_key=True)
    """Track each question attempt by user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_attempts')
    selected_text = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField()
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')  # One attempt per user per question
        indexes = [
            models.Index(fields=['user', 'question']),
            models.Index(fields=['user', 'is_correct']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.question}"

class UserChapterStats(models.Model):
    uc_id = models.AutoField(primary_key=True)
    """Cache statistics per user per chapter for fast queries"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chapter_stats')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='user_stats')
    
    total_questions = models.PositiveIntegerField(default=0)
    attempted = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)
    wrong = models.PositiveIntegerField(default=0)
    score_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    last_attempt = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'chapter')
        indexes = [
            models.Index(fields=['user', 'chapter']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.chapter.title} ({self.score_percentage}%)"
    
    @property
    def pending(self):
        return self.total_questions - self.attempted
    
    def update_stats(self):
        """Recalculate stats from UserQuestionAttempt records"""
        self.total_questions = self.chapter.questions.count()
        attempts = UserQuestionAttempt.objects.filter(
            user=self.user,
            question__chapter=self.chapter
        )
        self.attempted = attempts.count()
        self.correct = attempts.filter(is_correct=True).count()
        self.wrong = self.attempted - self.correct
        self.score_percentage = (self.correct / self.attempted * 100) if self.attempted > 0 else 0
        last_attempt = attempts.order_by('-attempted_at').first()
        self.last_attempt = last_attempt.attempted_at if last_attempt else None
        self.save()