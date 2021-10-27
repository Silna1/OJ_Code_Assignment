from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def nameFile(instance, filename):
    return '/'.join(['images', str(instance.image), filename])


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='', null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.description
