from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Contact, ContactNote
from .serializers import ContactSerializer, ContactNoteSerializer
from rest_framework.exceptions import NotFound
from django.utils.dateparse import parse_date
from authentication.permissions import IsOwnerOrManager


class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManager]
    # Removed lookup_field = 'id' to use default 'pk'

    def get_queryset(self):
        if self.request.user.role in ['manager', 'admin']:
            queryset = Contact.objects.all()
        else:
            queryset = Contact.objects.filter(owner=self.request.user)
    
        country_code = self.request.query_params.get('country_code')
        if country_code:
            queryset = queryset.filter(country_code__iexact=country_code)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get', 'post'], url_path='notes')
    def contact_notes(self, request, pk=None):
        # try:
        #     contact = Contact.objects.get(pk=pk, owner=request.user)
        # except Contact.DoesNotExist:
        #     raise NotFound("Contact not found.")

        try:
            contact = Contact.objects.get(pk=pk)
            if contact.owner != request.user and request.user.role not in ['admin', 'manager']:
                raise Contact.DoesNotExist
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
        user = self.request.user
        if user.role in ['manager', 'admin']:
            queryset = ContactNote.objects.all()
        else:
            queryset = ContactNote.objects.filter(contact__owner=user)
            
        
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(created_at__date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(created_at__date__lte=parse_date(end_date))

        return queryset
    
    @action(detail=False, methods=['delete'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.data.get("ids", [])
        if not isinstance(ids, list):
            return Response({"detail": "Invalid format. 'ids' must be a list."},
                            status=status.HTTP_400_BAD_REQUEST)

        deleted, _ = ContactNote.objects.filter(id__in=ids, contact__owner=request.user).delete()
        return Response({"deleted": deleted}, status=status.HTTP_200_OK)
