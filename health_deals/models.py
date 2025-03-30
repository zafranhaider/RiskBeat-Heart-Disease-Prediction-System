from django.db import models

# Create your models here.

class Notification(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='notifications/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
