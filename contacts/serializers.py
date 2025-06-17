# serializers.py
from rest_framework.serializers import ModelSerializer
from .models import Contact, ContactNote
from rest_framework import serializers

class ContactNoteSerializer(ModelSerializer):
    class Meta:
        model = ContactNote
        fields = '__all__'
        read_only_fields = ['contact']




class ContactSerializer(ModelSerializer):
    note_count = serializers.SerializerMethodField()
    notes = ContactNoteSerializer(many=True, read_only=True)
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'phone_number','country_code','contact_picture','is_favourited','note_count','notes']
        read_only_fields = ['owner']

    def get_note_count(self, obj):
        return obj.notes.count()

