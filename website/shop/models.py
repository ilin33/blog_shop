from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Назва")
    slug=models.SlugField(max_length=255, unique=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=['id','slug'],)
        ]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

