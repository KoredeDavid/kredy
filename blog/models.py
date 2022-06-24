from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from ckeditor.fields import RichTextField

from blog.validators import username_validator, author_validation, approved_by_validation, username_min_length


# This is to prevent unwanted characters so as not to disturb the web url
def clean_slug(value):
    clean_value = list(value)
    for i in clean_value:
        if not (i.isdigit() or i.isalpha() or i == ' '):
            clean_value.remove(i)
    return ''.join(clean_value)


class CustomUser(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=30,
        help_text=_('Letters, digits and underscore only.'),
        unique=True,
        validators=[username_validator, username_min_length],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=False, null=True, unique=True)
    is_author = models.BooleanField(default=False, )

    # This will be used for authors who are good enough not to need approval before their article gets published
    is_pro_author = models.BooleanField(default=False, )
    is_boss = models.BooleanField(default=False)

    def clean(self):
        # This raises a validation error because it makes no sense to make someone a pro_author if he/she aint an author
        if self.is_pro_author and not self.is_author:
            raise ValidationError({"is_pro_author": 'The user cannot be a professional author if he/she is not an '
                                                    'author'})

        if self.is_boss:
            self.is_author = True
            self.is_pro_author = True

        if self.email is not None:
            self.email = self.email.lower()

        """
            The reason for this custom validation is that since I am not using the clean method to lower the username
            but the save method, so the unique=True validator does not call in save method which, raises a UNIQUE 
            constraint error 
        """
        try:
            get_username = CustomUser.objects.get(username__iexact=self.username)
        except CustomUser.DoesNotExist:
            get_username = None

        if get_username:
            if get_username.id != self.id:
                raise ValidationError({'username': "User with this username already exists"})

    def save(self, *args, **kwargs):
        self.full_clean()


        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    about = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def clean(self):
        try:
            get_title = Category.objects.get(title__iexact=self.title)
        except Category.DoesNotExist:
            get_title = None

        if get_title:
            if get_title.id != self.id:
                raise ValidationError({'title': "Category with this title already exists"})

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.title is not None:
            self.slug = slugify(clean_slug(self.title.lower()))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    category = models.ForeignKey('Category', related_name='post', on_delete=models.CASCADE)
    title = models.CharField(unique=True, max_length=100)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, validators=[author_validation, ],
                 related_name='post_author', null=True)  #
    body = RichTextField()
    approved = models.BooleanField(default=False, )  #
    approved_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, validators=[approved_by_validation, ],
                                    related_name='post_approved_by', blank=True, null=True)  #
    published = models.BooleanField(default=False, )
    draft = models.BooleanField(default=False)  #
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)
    read = models.PositiveIntegerField(editable=False)

    def publish(self):
        self.draft = False
        self.published = True
        self.save()

    def save_as_draft(self):
        self.published = False
        self.draft = True
        self.save()

    def clean(self):
        if self.author:
            if self.author.is_pro_author:
                self.approved = True
        if (not self.approved or self.approved_by is None) and self.published:
            raise ValidationError({'published': "This post is yet to be approved by the boss, so it can't be published"})

        try:
            get_title = Post.objects.get(title__iexact=self.title)
        except Post.DoesNotExist:
            get_title = None

        if get_title:
            if get_title.id != self.id:
                raise ValidationError({'title': "Post with this title already exists"})

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.title is not None:
            self.slug = slugify(clean_slug(self.title.lower()))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Edit(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, )
    body = models.TextField()


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = RichTextField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.author
