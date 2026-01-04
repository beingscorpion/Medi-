from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from decimal import Decimal

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


# Past Paper Models
class Province(models.Model):
    p_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class PastPaperYear(models.Model):
    ppy_id = models.AutoField(primary_key=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='years')
    year = models.PositiveIntegerField()
    slug = models.SlugField(max_length=100)  # For URLs like 'punjab-2023'
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('province', 'year')
        ordering = ['province', '-year']
    
    def __str__(self):
        return f"{self.province.name} - {self.year}"

class PastPaperQuestion(models.Model):
    ppq_id = models.AutoField(primary_key=True)
    year = models.ForeignKey(PastPaperYear, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    
    # MCQ options
    key1 = models.CharField(max_length=255, blank=True, null=True)
    key2 = models.CharField(max_length=255, blank=True, null=True)
    key3 = models.CharField(max_length=255, blank=True, null=True)
    key4 = models.CharField(max_length=255, blank=True, null=True)
    
    # Correct answer (1-4 for MCQ)
    correct_text = models.CharField(max_length=255, blank=True, null=True)
    
    explanation = models.TextField(blank=True)
    report = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['year']),
        ]
    
    def __str__(self):
        return f"{self.year} - Q{self.ppq_id}"

class UserPastPaperAttempt(models.Model):
    uppa_id = models.AutoField(primary_key=True)
    """Track each past paper question attempt by user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='past_paper_attempts')
    question = models.ForeignKey(PastPaperQuestion, on_delete=models.CASCADE, related_name='user_attempts')
    selected_text = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField()
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')
        indexes = [
            models.Index(fields=['user', 'question']),
            models.Index(fields=['user', 'is_correct']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.question}"

class QuestionReport(models.Model):
    """Store detailed reports about questions with descriptions"""
    r_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_reports')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    past_paper_question = models.ForeignKey(PastPaperQuestion, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    description = models.TextField(help_text="Description of the issue with this question")
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['question']),
            models.Index(fields=['past_paper_question']),
        ]
    
    def __str__(self):
        question_ref = self.question if self.question else self.past_paper_question
        return f"Report by {self.user.username} - {question_ref}"


class ReferralCode(models.Model):
    """Referral/Coupon codes that users can share"""
    ref_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_codes')
    code = models.CharField(max_length=50, unique=True, help_text="Unique referral/coupon code")
    mobile_number = models.CharField(max_length=15, blank=True, null=True, help_text="Mobile number for commission payments")
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, help_text="Commission percentage for the referrer")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_uses = models.PositiveIntegerField(default=0, help_text="Total number of times this code has been used")
    total_commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Total commission earned from this code")
    
    class Meta:
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.user.username}"


class Payment(models.Model):
    """Payment submissions by users"""
    p_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Payment amount")
    transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="Transaction ID or reference number")
    payment_method = models.CharField(max_length=50, blank=True, null=True, help_text="Payment method (e.g., Bank Transfer, JazzCash, EasyPaisa)")
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True, help_text="Screenshot of payment proof")
    additional_details = models.TextField(blank=True, null=True, help_text="Any additional payment details")
    referral_code = models.ForeignKey(ReferralCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments', help_text="Referral/coupon code used")
    referrer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_payments', help_text="User who referred this payment")
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Commission amount for the referrer")
    commission_paid = models.BooleanField(default=False, help_text="Whether commission has been paid to referrer")
    confirmed = models.BooleanField(default=False, help_text="Manually confirmed after checking payment screenshot")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['confirmed']),
            models.Index(fields=['referral_code']),
            models.Index(fields=['referrer']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment by {self.user.username} - Rs. {self.amount} - {'Confirmed' if self.confirmed else 'Pending'}"
    
    def save(self, *args, **kwargs):
        # Check if this is an update and confirmed status changed
        if self.pk:
            try:
                old_instance = Payment.objects.get(pk=self.pk)
                was_confirmed = old_instance.confirmed
            except Payment.DoesNotExist:
                was_confirmed = False
        else:
            was_confirmed = False
        
        # Calculate commission if referral code is used
        if self.referral_code and not self.commission_amount:
            commission_percentage = self.referral_code.commission_percentage
            self.commission_amount = (Decimal(str(self.amount)) * Decimal(str(commission_percentage))) / Decimal('100')
        
        super().save(*args, **kwargs)
        
        # Update referral code stats when payment is confirmed
        if self.confirmed and not was_confirmed and self.referral_code:
            # Increment total uses only when payment is confirmed
            self.referral_code.total_uses += 1
            # Update commission earned
            if self.commission_amount:
                self.referral_code.total_commission_earned = Decimal(str(self.referral_code.total_commission_earned)) + Decimal(str(self.commission_amount))
            self.referral_code.save(update_fields=['total_uses', 'total_commission_earned'])