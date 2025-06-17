from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Contact, ContactNote
from .serializers import ContactSerializer, ContactNoteSerializer
from rest_framework.exceptions import NotFound

class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    # Removed lookup_field = 'id' to use default 'pk'

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get', 'post'], url_path='notes')
    def contact_notes(self, request, pk=None):
        try:
            contact = Contact.objects.get(pk=pk, owner=request.user)
        except Contact.DoesNotExist:
            raise NotFound("Contact not found.")

        if request.method == 'POST':
            serializer = ContactNoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(contact=contact)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  # GET
            notes = contact.notes.all()
            serializer = ContactNoteSerializer(notes, many=True)
            return Response(serializer.data)


class ContactNoteViewSet(ModelViewSet):
    serializer_class = ContactNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContactNote.objects.filter(contact__owner=self.request.user)
