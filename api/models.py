#
# Copyright (C) 2014 Shang Yuanchun <idealities@gmail.com>
#

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)
from django.utils import timezone

class UserManager(BaseUserManager):

    def _create_user(self, username, email, avatar,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email, password and
        avatar.

        """

        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        if avatar is None:
            from api.util import make_default_avatar
            avatar = make_default_avatar(email)
        user  = self.model(username=username, email=email, avatar=avatar,
                           is_staff=is_staff, is_active=True,
                           is_superuser=is_superuser, last_login=now,
                           date_joined=now, **extra_fields)
        user.set_password(self.make_random_password())
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, avatar=None, **extra_fields):
        """
        """
        return self._create_user(username, email, avatar,
                                 False, False, **extra_fields)

    def create_superuser(self, username, email, avatar=None, **extra_fields):
        """
        """
        return self._create_user(username, email, avatar,
                                 True, True, **extra_fields)

class User(AbstractUser):

    # add a avatar, retrived from social account
    avatar = models.URLField(default='')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Comment(models.Model):

    TYPE_NORMAL = 1
    TYPE_REPLY  = 2

    comment_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0, db_index=True)
    comment_page = models.URLField(default='', db_index=True)
    comment_type = models.SmallIntegerField(help_text='1: normal comment, 2: reply', default=1)
    comment_date = models.DateTimeField(help_text='date published')
    comment_content = models.TextField(max_length=4096)
    comment_ups = models.IntegerField(default=0)
    comment_downs = models.IntegerField(default=0)
    comment_parent = models.BigIntegerField(default=0)

