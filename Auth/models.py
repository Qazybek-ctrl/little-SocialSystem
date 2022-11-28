from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class SocialPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, db_index=True, max_length=255, verbose_name='URL')
    info = models.CharField(max_length=500, blank=True)
    age = models.IntegerField(blank=True, null=True, default=None)
    job = models.CharField(max_length=150, blank=True, default="")
    photo = models.ImageField(upload_to=user_directory_path, blank=True, default='')
    back = models.ImageField(upload_to=user_directory_path, blank=True, default='')
    phone = models.CharField(max_length=15, default="", blank=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    github = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_slug': self.slug})
