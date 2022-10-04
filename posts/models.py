import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class PostCategory(models.Model):
    '''Категории постов'''
    name = models.CharField(_('Category name'), unique=True, max_length=100)

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


def default_category():
    """На случай если пользователь не выберит категорию
    в момент публикации"""
    return PostCategory.objects.get_or_create(name='Прочее')[0]


class Post(models.Model):
    """Модель публикации"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(PostCategory, on_delete=models.SET(default_category))
    title = models.CharField(max_length=200)
    body = models.TextField()
    picture = models.ImageField(upload_to='picture/%Y/%m/%d', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-created',)

    def get_total_number_of_likes(self):
        return self.postlike_set.count()

    def get_total_number_of_bookmarks(self):
        return self.bookmarks_set.count()

    def __str__(self):
        return f'Post: {self.id}, by {self.author.username}'


class PostLike(models.Model):
    """Модель лайков"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        ordering = ('-created',)

    def __str__(self):
        return self.user.username
