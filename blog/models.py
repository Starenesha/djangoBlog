from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug +"-"+str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True )
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag',related_name='posts',
                                  blank=True)  # blank=True означает что это поле необязательное к заполнению

    def get_absolute_url(self):
        return reverse('post_detail_url',kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args,**kwargs)

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug':self.slug})

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['title']

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

        def create_user(self, email, password=None, **extra_fields):
            """Create and save a regular User with the given email and password."""
            extra_fields.setdefault('is_staff', False)
            extra_fields.setdefault('is_superuser', False)
            return self._create_user(email, password, **extra_fields)

        def create_superuser(self, email, password, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_active', True)

            if extra_fields.get('is_staff') is not True:
                raise ValueError('Superuser must have is_staff=True.')
            if extra_fields.get('is_superuser') is not True:
                raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

