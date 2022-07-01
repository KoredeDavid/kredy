import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

from ckeditor.fields import RichTextField

from my_blog.validators import case_insensitive_unique_validator

UserModel = get_user_model()


def clean_slug(value):
    """
    It cleans the slug value so that it contains only alphanum characters
    """
    clean_value = list(value)
    for i in clean_value:
        if not (i.isdigit() or i.isalpha() or i == ' '):
            clean_value.remove(i)
    return ''.join(clean_value)


# Models

class Author(models.Model):
    clean_method_is_called = False

    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(UserModel, on_delete=models.SET_NULL, null=True)
    is_pro_author = models.BooleanField(default=False)
    is_boss = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def clean(self):
        self.clean_method_is_called = True

        if self.is_boss:
            self.is_pro_author = True

    def save(self, *args, **kwargs):
        if not self.clean_method_is_called:
            self.full_clean()

            super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    clean_method_is_called = False

    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=50, unique=True)
    about = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def clean(self):
        self.clean_method_is_called = True

        case_insensitive_unique_validator(self, 'title', self.title)

    def save(self, *args, **kwargs):
        if not self.clean_method_is_called:
            self.full_clean()

        if self.title is not None:
            self.slug = slugify(clean_slug(self.title.lower()))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    clean_method_is_called = False

    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    post_category = models.ForeignKey('Category', related_name='post_category', on_delete=models.SET_NULL, null=True)
    title = models.CharField(unique=True, max_length=100)
    post_author = models.ForeignKey('Author', on_delete=models.SET_NULL, related_name='post_author', null=True)
    body = RichTextField()
    approved = models.BooleanField(default=False, )
    approved_by = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='post_approved_by', blank=True,
                                    null=True)
    published = models.BooleanField(default=False, )
    draft = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)
    amount_of_times_read = models.PositiveIntegerField(editable=False)

    def publish(self):
        self.draft = False
        self.published = True
        self.save()

    def save_as_draft(self):
        self.published = False
        self.draft = True
        self.save()

    def clean(self):
        self.clean_method_is_called = True

        if self.post_author:
            if self.post_author.is_pro_author:
                self.approved = True

        if self.approved_by:
            if not self.approved_by.is_boss:
                raise ValidationError('Posts can only be approved by bosses')

        if (not self.approved or self.approved_by is None) and self.published:
            raise ValidationError(
                {'published': "This post is yet to be approved by the boss, so it can't be published"})

        case_insensitive_unique_validator(self, 'title', self.title)

    def save(self, *args, **kwargs):
        if not self.clean_method_is_called:
            self.full_clean()

        if self.title is not None:
            self.slug = slugify(clean_slug(self.title.lower()))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Edit(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    edit_post = models.ForeignKey('Post', related_name='post_edit', on_delete=models.SET_NULL, null=True)
    body = models.TextField()


class Comment(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    comment_author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='user_comment', null=True)
    body = RichTextField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    comment_post = models.ForeignKey('Post', on_delete=models.SET_NULL, related_name='post_comment', null=True)

    def __str__(self):
        return self.comment_author
