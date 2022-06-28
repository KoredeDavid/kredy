from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CustomUserCreationForm, PostForm
from .models import Post, Category, Comment



@login_required
def articles_factory(request, username):
    if request.user.is_author:
        print(request.user)
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                print(request.POST)
                if 'save_as_draft' in request.POST:
                    form_instance = form.save(commit=False)
                    form_instance.author = request.user
                    form_instance.save_as_draft()
                if 'save' in request.POST and (request.user.is_pro_author or request.user.is_boss):
                    form_instance = form.save(commit=False)
                    form_instance.author = request.user
                    form_instance.approved_by = request.user
                    form_instance.approved = True
                    form_instance.publish()
                if 'send_for_approval' in request.POST and (not request.user.is_pro_author or not request.user.is_boss):
                    pass

                return redirect("articles_factory")
        else:
            form = PostForm()
        posts = Post.objects.all()

        context = {
            'form': form,
            'posts': posts
        }

        return render(request, 'blog/articles_factory.html', context)
    else:
        raise PermissionDenied


