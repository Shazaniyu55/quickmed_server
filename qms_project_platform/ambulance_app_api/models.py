from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets





class AmbulanceSessionModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @classmethod
    def create_session(cls, user_id):
        token = secrets.token_hex(32)  # Generate a random token
        session = cls.objects.create(user_id=user_id, token=token, expires_at=timezone.now() + timedelta(days=7))
        return session.token



class AmbulanceAPIKeyModel(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key



    @classmethod
    def generate_key(cls):
        key = secrets.token_urlsafe(32) 
        return key

    




