from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from .models import Profile

CustomUser = get_user_model()


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """Создаем профиль при создании модели User"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    """Сохраняем профиль в модели User"""
    instance.profile.save()
