from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Blog(models.Model):
    """Статьи публикуемые на сайте"""
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, db_index=True)
    body = models.TextField(max_length=2000, verbose_name='Содержание статьи')
    added = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    image = models.ImageField(upload_to='blog/')
    tags = TaggableManager()

    class Meta:
        verbose_name_plural = 'Статьи'
        verbose_name = 'Статья'
        ordering = ['-added']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.slug])

class Comment(models.Model):
    article = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, verbose_name='имя', blank=False)
    email = models.EmailField(null=True, blank=False)
    body = models.TextField(max_length=300, verbose_name='содержимое', blank=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Был добавлен')
    updated = models.DateTimeField(auto_now=True, verbose_name='Был изменен')

    class Meta:
        ordering = ['created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment by {self.name}'
