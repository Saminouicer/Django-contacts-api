# contacts/urls.py
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, ContactNoteViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contacts')
router.register(r'notes', ContactNoteViewSet, basename='notes')

urlpatterns = router.urls
