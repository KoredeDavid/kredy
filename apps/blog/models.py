import re
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from ckeditor.fields import RichTextField
from my_blog.models_manger import MyModelManager

UserModel = get_user_model()

# Regex pattern for cleaning blog title and category
pattern = re.compile(r'[^ A-Za-z0-9 ]+')


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
    # This Custom Model manager ensures case insensitive unique fields
    objects = MyModelManager('title')

    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=50, unique=True)
    about = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if self.title is not None:
            self.slug = slugify(re.sub(pattern, '', self.title.lower()))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    A post has to be approved before published. A post by a pro_author or a boss does not need approval.
    Also, a post can only be approved by a boss. The clean() method ensures this.
    """

    # This Custom Model manager ensures case insensitive unique fields
    objects = MyModelManager('title')

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

    bookmarks = models.ManyToManyField(UserModel, related_name='bookmarked_by', blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)

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
                raise ValidationError({'approved_by': 'Posts can only be approved by bosses'})

        if not self.post_author.is_pro_author:
            if (not self.approved or self.approved_by is None) and self.published:
                raise ValidationError(
                    {'published': "This post is yet to be approved by the boss, so it can't be published"})

    def save(self, *args, **kwargs):
        if not self.clean_method_is_called:
            self.full_clean()

        if self.title is not None:
            self.slug = slugify(re.sub(pattern, '', self.title.lower()))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostRead(models.Model):
    post_read = models.ForeignKey('Post', related_name='post_read', on_delete=models.SET_NULL, null=True)
    read_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='read_by', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Posts Read'

    def __str__(self):
        return f'{self.read_by} read {self.post_read.slug}'


class PostReaction(models.Model):
    LIKE = 'LI'
    LOVE = 'LO'
    FUNNY = 'FU'
    SAD = 'SA'
    ANGRY = 'AN'
    SPEECHLESS = 'SP'

    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (LOVE, 'Love'),
        (FUNNY, 'Funny'),
        (SAD, 'Sad'),
        (ANGRY, 'Angry'),
        (SPEECHLESS, 'Speechless')
    ]
    post = models.ForeignKey('Post', related_name='reacted_post', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserModel, related_name='reacted_by', on_delete=models.SET_NULL, null=True)
    reaction = models.CharField(max_length=2, choices=REACTION_CHOICES, default=LIKE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['post', 'user'], name='post_user_unique')]

    def __str__(self):
        return f'{self.user} reacts to {self.post}, {self.reaction}'


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



"""
# add 'read_count' to attribute
>>> users = CustomUser.objects.annotate(read_count=Count('read_by'))
# filter read_count whose attribute is > 0
>>> user_who_read_post  = users.filter(read_count__gt=0)
>>> k = user_who_read_post[1]
>>> k.username
'KoredeDavid'
>>> k.email
'koredeoluwashola@gmail.com'
>>> k.uuid
UUID('56eb9e4c-d121-4d1c-99b0-4e2eb544d2c9')
>>> k.read_count
3

>>> PostRead.objects.filter(read_by=k).values_list('post_read__post_category__title').annotate(read_count=Count('post_read__post_category__id')).order_by('-read_count')
<QuerySet [('This Is Me', 3), ('Naira Life', 3), ('Sex Life', 2)]>
>>> PostRead.objects.filter(read_by=k).values_list('post_read__post_category__id').annotate(read_count=Count('post_read__post_category__title')).order_by('-read_count')
<QuerySet [(5, 3), (2, 3), (1, 2)]>
>>> PostRead.objects.filter(read_by=k).values_list('post_read__post_category__title').annotate(read_count=Count('post_read__post_category__title')).order_by('-read_count')
<QuerySet [('This Is Me', 3), ('Naira Life', 3), ('Sex Life', 2)]>
>>> Category.objects.all().values_list('id')
<QuerySet [(1,), (3,), (5,), (2,), (4,)]>
>>> Category.objects.all().values_list('id', flat=True)
<QuerySet [1, 3, 5, 2, 4]>
>>> PostRead.objects.filter(read_by=k).values_list('post_read__post_category__id').annotate(read_count=Count('post_read__post_category__id')).order_by('-read_count')
<QuerySet [(5, 3), (2, 3), (1, 2)]>
>>> PostRead.objects.filter(read_by=k).values_list('post_read__post_category__id', flat=True).annotate(read_count=Count('post_read__post_category__id')).order_by('-read_count')
<QuerySet [5, 2, 1]>
>>> ex = list(PostRead.objects.filter(read_by=k).values_list('post_read__post_category__id', flat=True).annotate(read_count=Count('post_read__post_category__id')).order_by('-read_count'))
>>> ex
[5, 2, 1]
>>> Category.objects.exclude(id__in=ex)
<QuerySet [<Category: School Life>, <Category: A week in life>]>
>>> Category.objects.exclude(id__in=ex).values_list('id', flat=True)
<QuerySet [3, 4]>
>>> rem = Category.objects.exclude(id__in=ex)
>>> rem = list(rem)
>>> rem
[<Category: School Life>, <Category: A week in life>]
>>> rem = list(Category.objects.exclude(id__in=ex).values_list('id', flat=True))
>>> rem
[3, 4]
>>> ex
[5, 2, 1]
>>> ex+rem
[5, 2, 1, 3, 4]
>>> Category.Objects.all()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: type object 'Category' has no attribute 'Objects'
>>> Category.objects.all()
<QuerySet [<Category: Sex Life>, <Category: Naira Life>, <Category: School Life>, <Category: A week in life>, <Category: This Is Me>]>
>>> all = ex+rem

"""