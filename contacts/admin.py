from django.contrib import admin
from .models import Contact, ContactNote

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'country_code', 'owner', 'is_favourited')
    search_fields = ('first_name', 'last_name', 'phone_number', 'owner__username')
    list_filter = ('country_code', 'is_favourited')


class ContactNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact', 'title', 'created_at')
    search_fields = ('title', 'content', 'contact__first_name', 'contact__last_name')
    list_filter = ('created_at',)


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactNote, ContactNoteAdmin)
