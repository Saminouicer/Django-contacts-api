from django.db import models
from django.conf import settings
# Create your models here.

class Contact(models.Model):
    owner=models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    phone_number=models.CharField(max_length=30)
    country_code=models.CharField(max_length=30)
    contact_picture=models.URLField(null=True)
    is_favourited=models.BooleanField(default=True)

    def __str__(self):
        return self.owner.first_name




class ContactNote(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.contact.first_name} - {self.title}"

