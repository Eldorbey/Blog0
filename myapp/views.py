from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Blog, Category, Tag, User
from .forms import RegisterForm, BlogForm, CommentForm
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage

def home(request):
    blogs = Blog.objects.all()

    paginator =Paginator(blogs, 2)
    page_num = request.GET.get('page')

    page_obj = paginator.get_page(page_num)

    context = {
        'blogs': page_obj,
    }


    return render(request, 'home.html', context)

def category_blogs(request, slug):
    category = Category.objects.get(slug=slug)
    blogs = Blog.objects.filter(category=category)

    context = {
        'category':category,
        'blogs':blogs,
    }

    return render(request, 'category_blogs.html', context)

def category_list(request):
    category_list = Category.objects.all()
    tags = Tag.objects.all()

    context ={
        'category_list': category_list,
    }

    return render(request, 'category_list.html', context)

def tag_blogs(request, slug):
    tag = Tag.objects.get(slug=slug)
    blogs = Blog.objects.filter(tags=tag)

    context = {
        'tag':tag,
        'blogs': blogs
    }

    return render(request, 'tag_blogs.html', context)

def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.blog = blog
            form2.user = request.user
            form2.save()
            return redirect('blog_detail', blog.slug)
    else:
        form = CommentForm()


    context = {
        'blog': blog,
        'form': form,

    }

    return render(request, 'blog_detail.html', context)

def login_page(request):
    form = AuthenticationForm()
    if request.method == 'PSOT':
        form = AuthenticationForm(date=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            mess = "Username yoki password xato"

    context = {
        'form': form,
    }

    return render(request, 'login_page.html', context)

def logout_page(request):
    logout(request)
    return redirect('login_page')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'register.html', context)

def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.slug = slugify(form2.title)
            form2.user = request.user
            form2.save()
            blog =Blog.objects.get(id=form2.id)
            tags = form.cleaned_data.get('tags')
            tag_list = list(tags.split(','))
            for tag in tag_list:
                tag, create = Tag.objects.get_or_create(name=tag.strip())
                blog.tags.add(tag)
            return redirect('home')

    else:
        form = BlogForm()

    context = {
        'form': form,
    }

    return render(request, 'blog_create.html', context)



def blog_update(request, slug):
    blog = Blog.objects.get(slug=slug)
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        form.save()
        return redirect('blog_detail', blog.slug)

    context = {
        'blog':blog,
        'form':form,
    }

    return render(request, 'blog_update.html', context)

def blog_delete(request, slug):
    blog = Blog.objects.get(slug=slug)
    if request.method == 'Post':
        blog.delete()
        return redirect()


    context ={

        'blog':blog,
    }

    return render(request, 'blog_delete.html', context)

def user_list(request):

    username = request.GET.get('qidiruv')
    if username:
        users = User.objects.filter(username__icontains=username)

    else:
        users = User.objects.all()

    context = {
        'users': users
    }

    return render(request, 'user_list.html', context)



















