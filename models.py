from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField("Категория", max_length=100)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField("Содержание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    categories = models.ManyToManyField(Category, blank=True, verbose_name="Категории")

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="Статья")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField("Текст комментария")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author} к статье {self.article}"