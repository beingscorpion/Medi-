from django.contrib import admin
from home.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.
admin.site.unregister(User)

class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'message')
    search_fields = ('name', 'phone', 'message')
    list_filter = ('name',)

    # def short_message(self, obj):
    #     return (obj.message[:75] + '...') if len(obj.message) > 75 else obj.message

    # short_message.short_description = 'Message'


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('s_id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('c_id', 'subject', 'chapter_no', 'title', 'slug')
    search_fields = ('title', 'slug')
    list_filter = ('subject', 'chapter_no')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('q_id', 'chapter', 'paper_type', 'question' , 'key1', 'key2', 'key3', 'key4', 'correct_text', 'report',)
    search_fields = ('question',)
    list_filter = ('chapter', 'paper_type')

class UserQuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ('uq_id', 'user', 'question', 'selected_text', 'is_correct', 'attempted_at')
    search_fields = ('user', 'question')
    list_filter = ('user', 'question', 'is_correct')

class UserChapterStatsAdmin(admin.ModelAdmin):
    list_display = ('uc_id', 'user', 'chapter', 'total_questions', 'attempted', 'correct', 'wrong', 'score_percentage', 'last_attempt')
    search_fields = ('user', 'chapter')
    list_filter = ('user', 'chapter')

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('p_id', 'name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

class PastPaperYearAdmin(admin.ModelAdmin):
    list_display = ('ppy_id', 'province', 'year', 'slug')
    search_fields = ('province__name', 'year', 'slug')
    list_filter = ('province', 'year')

class PastPaperQuestionAdmin(admin.ModelAdmin):
    list_display = ('ppq_id', 'year', 'question', 'key1', 'key2', 'key3', 'key4', 'correct_text', 'report')
    search_fields = ('question',)
    list_filter = ('year', 'report')

class UserPastPaperAttemptAdmin(admin.ModelAdmin):
    list_display = ('uppa_id', 'user', 'question', 'selected_text', 'is_correct', 'attempted_at')
    search_fields = ('user', 'question')
    list_filter = ('user', 'question', 'is_correct')

class QuestionReportAdmin(admin.ModelAdmin):
    list_display = ('r_id', 'user', 'question', 'past_paper_question', 'description', 'resolved', 'created_at')
    search_fields = ('user__username', 'description', 'question__question', 'past_paper_question__question')
    list_filter = ('resolved', 'created_at', 'question', 'past_paper_question')
    readonly_fields = ('created_at',)
    list_editable = ('resolved',)
    
    # def get_question(self, obj):
    #     if obj.question:
    #         return f"Q{obj.question.q_id}: {obj.question.question[:50]}..."
    #     elif obj.past_paper_question:
    #         return f"PPQ{obj.past_paper_question.ppq_id}: {obj.past_paper_question.question[:50]}..."
    #     return "N/A"
    # get_question.short_description = 'Question'

class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('ref_id', 'user', 'code', 'mobile_number', 'commission_percentage', 'is_active', 'total_uses', 'total_commission_earned', 'created_at')
    search_fields = ('code', 'user__username', 'user__email', 'mobile_number')
    list_filter = ('is_active', 'created_at', 'commission_percentage')
    readonly_fields = ('total_uses', 'created_at')
    list_editable = ('is_active',)
    fieldsets = (
        ('Code Information', {
            'fields': ('user', 'code', 'mobile_number', 'is_active')
        }),
        ('Commission Settings', {
            'fields': ('commission_percentage',)
        }),
        ('Statistics', {
            'fields': ('total_uses', 'total_commission_earned', 'created_at'),
            'description': 'Note: You can edit "Total Commission Earned" to reset it after paying the referrer.'
        }),
    )

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('p_id', 'user', 'amount', 'screenshot_thumbnail', 'transaction_id', 'payment_method', 'referral_code', 'referrer', 'commission_amount', 'confirmed', 'commission_paid', 'created_at')
    search_fields = ('user__username', 'transaction_id', 'referral_code__code')
    list_filter = ('confirmed', 'commission_paid', 'payment_method', 'created_at', 'referral_code')
    readonly_fields = ('created_at', 'updated_at', 'commission_amount', 'screenshot_preview')
    list_editable = ('confirmed', 'commission_paid')
    fieldsets = (
        ('Payment Information', {
            'fields': ('user', 'amount', 'transaction_id', 'payment_method', 'payment_screenshot', 'screenshot_preview', 'additional_details')
        }),
        ('Referral Information', {
            'fields': ('referral_code', 'referrer', 'commission_amount', 'commission_paid')
        }),
        ('Status', {
            'fields': ('confirmed', 'created_at', 'updated_at')
        }),
    )
    
    def screenshot_thumbnail(self, obj):
        if obj.payment_screenshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px; cursor: pointer;" /></a>',
                obj.payment_screenshot.url,
                obj.payment_screenshot.url
            )
        return "No Screenshot"
    screenshot_thumbnail.short_description = 'Screenshot'
    
    def screenshot_preview(self, obj):
        if obj.payment_screenshot:
            return format_html(
                '<img src="{}" style="max-width: 600px; max-height: 600px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.payment_screenshot.url
            )
        return "No screenshot uploaded"
    screenshot_preview.short_description = 'Screenshot Preview'

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserQuestionAttempt, UserQuestionAttemptAdmin)
admin.site.register(UserChapterStats, UserChapterStatsAdmin)
admin.site.register(Contact, ContactFormAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(PastPaperYear, PastPaperYearAdmin)
admin.site.register(PastPaperQuestion, PastPaperQuestionAdmin)
admin.site.register(UserPastPaperAttempt, UserPastPaperAttemptAdmin)
admin.site.register(QuestionReport, QuestionReportAdmin)
admin.site.register(ReferralCode, ReferralCodeAdmin)
admin.site.register(Payment, PaymentAdmin)
