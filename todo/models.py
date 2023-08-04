from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class ToDo(BaseModel):
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название', max_length=64)
    description = models.TextField(verbose_name='Описание', blank=True, max_length=4096)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    achieve_date = models.DateTimeField(verbose_name='Дата выполнения', null=True, blank=True)
    important = models.BooleanField(verbose_name='Важно', default=False)

    def __str__(self):
        return self.title
