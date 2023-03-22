from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)  # Header
    body = models.TextField(blank=True, null=True)  # Body
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    is_trashed = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ("title",)
