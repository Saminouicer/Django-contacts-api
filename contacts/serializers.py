# serializers.py
from rest_framework.serializers import ModelSerializer
from .models import Contact, ContactNote

class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['owner']

class ContactNoteSerializer(ModelSerializer):
    class Meta:
        model = ContactNote
        fields = '__all__'
        read_only_fields = ['contact']
