from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .models import Post, Category, UserProfile, Tag
from .forms import PostForm, CommentForm, UserForm, UserProfileForm, RegistrationForm



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


def category(request, name):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)

def tag(request, name):
    t = get_object_or_404(Tag, name=name)
    posts = Post.objects.filter(tags=t).order_by('-published_date')
    context = {'posts': posts, 'current_tag': t}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)

# @login_required
# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.published_date = now()
#             post.save()
#             return index(request)
#     create_form = PostForm()
#     context = {'create_form': create_form}
#     context.update(get_categories())
#     return render(request, "blog/create.html", context)
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Автор поста
            post.published_date = now()
            post.save()
            return redirect('my_posts')
    else:
        form = PostForm()

    context = {'create_form': form}
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


@login_required
def update_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профіль успішно оновлено!')
            return redirect('profile')  # або 'update_profile' якщо хочеш залишитись
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    context.update(get_categories())  # якщо потрібно відображати категорії
    return render(request, 'blog/update_profile.html', context)


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

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    context.update(get_categories())  # ← додай це

    return render(request, 'blog/post.html', context)

@login_required
def my_posts(request):
    posts = Post.objects.filter(user=request.user).order_by('-published_date')
    context = {'posts': posts}
    context.update(get_categories())  # якщо ти показуєш категорії
    return render(request, 'blog/my_post.html', context)

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, user=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Пост успішно видалено.")
        return redirect('my_posts')

    return render(request, 'blog/confirm_delete.html', {'post': post})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)  # тільки свої пости

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_posts')
    else:
        form = PostForm(instance=post)

    context = {'form': form, 'post': post}
    return render(request, 'blog/edit_post.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # перенаправляємо на сторінку входу
    else:
        form = RegistrationForm()

    return render(request, 'blog/registration_user.html', {'form': form})