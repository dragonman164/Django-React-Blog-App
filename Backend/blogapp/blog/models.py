from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    is_member = models.BooleanField(default = False)

# In Future, Add Profile Picture Section
class BlogUser(models.Model):
    GENDER_CHOICES = (
        ("Male","Male"),
        ("Female","Female"),
        ("TransGender","TransGender")
    )

    name = models.CharField(null = False, blank = False, max_length=100)
    email = models.EmailField(null = False, blank = False, unique=True)
    phoneno = models.CharField(null = False, blank = False, max_length = 12)
    address = models.CharField(null = True, blank = True, max_length = 500)
    profession = models.CharField(null = True, blank = True, max_length=100)
    member = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    dob = models.DateField(null = True, blank = True)
    gender = models.CharField(max_length=20, null = False, blank = False, 
            choices=GENDER_CHOICES)
    


# In Future, Add Images Upload Section
class Blog(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, blank = False, null = False)
    topic = models.CharField(null = False, blank = False, max_length = 50)
    timeofcreation = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null = True, blank = True, max_length=5000)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank = False, null = False)
    user = models.OneToOneField(BlogUser, on_delete=models.CASCADE, blank = False, null = False)
    timeofcreation = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null = False, blank = False, max_length = 1000)

class LikeDisklike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null = False, blank = False)
    user = models.OneToOneField(BlogUser, on_delete=models.CASCADE, null = False, blank = False)
    like = models.BooleanField(default= False, null = False, blank = False)
    dislike = models.BooleanField(default=False, null = False, blank = False)

