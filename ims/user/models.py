from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=20, null=True)
    jobTitle = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)
    division = models.CharField(max_length=200, null=True)
    image = models.ImageField(default='avatar.jpg', upload_to='Profile_Images')

    def __str__(self):
        return f'{self.user.username}-Profile'
