from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .models import Post, Category, UserProfile, Comment
from .forms import PostForm, CommentForm


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2
    return {'cats1': all[:half], 'cats2': all[half:]}


def index(request):
    posts = Post.objects.all().order_by('-published_date')
    # posts = Post.objects.filter(title__contains='django1')
    # posts = Post.objects.filter(published_date__year=2025)
    # posts = Post.objects.filter(published_date__month=1, published_date__year=2024)
    # posts = Post.objects.filter(category__name__exact="django")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def post(request, title):
    post = get_object_or_404(Post, slug=title)
    context = {'post': post}
    context.update(get_categories())
    return render(request, "blog/post.html", context)


def category(request, name):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.save()
            return index(request)
    create_form = PostForm()
    context = {'create_form': create_form}
    context.update(get_categories())
    return render(request, "blog/create.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Якщо користувач уже ввійшов, перенаправити на профіль

    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')  # Успішний вхід -> профіль
        else:
            messages.error(request, "Invalid username or password")
            return redirect('index')

    return render(request, 'blog/login.html')  # Показуємо сторінку логіну

def logout_view(request):
    logout(request)
    return redirect('index')  # Повертаємо на сторінку входу



@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'blog/profile.html', {'profile': profile})


def post(request, title):
    post = get_object_or_404(Post, slug=title)
    comments = post.comments.select_related('user').order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post', title=post.slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })