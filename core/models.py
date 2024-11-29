from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Download(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField()
    format_id = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    file_size = models.BigIntegerField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    download_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']