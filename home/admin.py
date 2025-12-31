from django.contrib import admin
from home.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
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
