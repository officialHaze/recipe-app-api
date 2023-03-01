from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


def normalized_email(email):
        index_of_at_the_rate = email.find('@')
        sliced_part_before_at = email[0:index_of_at_the_rate+1]
        sliced_part_after_at = email[index_of_at_the_rate+1:].lower()
        normalized_email = sliced_part_before_at + sliced_part_after_at

        return normalized_email


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=normalized_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

