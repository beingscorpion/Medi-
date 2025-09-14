from django.contrib import admin
from home.models import Contact

# Register your models here.


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'message')
    search_fields = ('name', 'phone', 'message')
    list_filter = ('name',)

    # def short_message(self, obj):
    #     return (obj.message[:75] + '...') if len(obj.message) > 75 else obj.message

    # short_message.short_description = 'Message'


admin.site.register(Contact , ContactFormAdmin)