from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from cloudinary.models import CloudinaryField

# Create your models here.


# class CustomUser(AbstractUser):
#     pass
#     # is_manager = models.BooleanField("Is Manager", default=False)

#     def __str__(self):
#         return self.username


class Profile(models.Model):
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=6, choices=GENDER, default='male')
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(blank=True, max_length=20)
    company = models.CharField(null=True, blank=True, max_length=100)
    avatar = CloudinaryField('image', default='https://res.cloudinary.com/dyrp3aqdq/image/upload/v1644094165/userimage_j61wqm.png')#models.ImageField(blank=True, upload_to="profile_pics/", default="/userimage.png") 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)

    def image_tag(self):
        if self.avatar:
            return mark_safe('<img src="%s" height="50" width="50">' %self.avatar.url)
        return "No image found"
    image_tag.short_description = 'Avatar'