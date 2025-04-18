from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Тег")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Дата та час публікації")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Автор")
    image = models.URLField(default="https://fraserbond.com/oc-content/plugins/blog/img/blog/blog-default.png")
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новина"
        verbose_name_plural = "Новини"


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    caption = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Image for {self.post.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    content = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата коментаря")

    def __str__(self):
        return f"Коментар від {self.user.username} до {self.post.title}"

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Телефон
    location = models.CharField(max_length=100, blank=True, null=True)  # Місцезнаходження
    birth_date = models.DateField(blank=True, null=True)  # Дата народження

    def __str__(self):
        return self.user.username


class SliderImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='slider_images/')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or f"Slide {self.pk}"
