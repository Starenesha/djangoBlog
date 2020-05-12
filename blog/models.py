from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from ckeditor.fields import RichTextField


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + "-" + str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True )
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = RichTextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag',related_name='posts', blank=True)
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE, verbose_name="Author", default=1)
    article_image = models.FileField(blank=True, null=True, verbose_name="attachment")

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args,**kwargs)

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug':self.slug})

    def get_author(self):
        return

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

