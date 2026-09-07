import uuid

from django.db import models


class UserModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )
    password_hash = models.CharField(
        max_length=255,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
    
    @property
    def is_authenticated(self):
        return True


    @property
    def is_anonymous(self):
        return False