from django.contrib import admin

from .models import Post, Category, Tag, Comment, SliderImage, PostImage

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')  # Колонки в адмінці
    ordering = ('order',)              # Сортування за полем "order"



admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(PostImage)
