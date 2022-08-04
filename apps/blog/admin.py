from django.contrib import admin
from .models import Category, Post, Comment, PostReaction, PostRead, Author

# Register your models here.

# admin.site.register(Project)

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)

admin.site.register(PostReaction)
admin.site.register(PostRead)
