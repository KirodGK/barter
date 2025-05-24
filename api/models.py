from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from barter_system.constant import CONDITION_VALUES, STATUS_VALUES


class Announcement(models.Model):
    title = models.TextField(verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image_url = models.TextField(null=True, verbose_name='Ссылка на изображение')
    category = models.CharField(max_length=100, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.CharField(
        choices=CONDITION_VALUES,
        default='used',
        max_length=100,
        verbose_name='Состояние'
    )

    # def clean(self):
    #     if self.user == self.author:
    #         raise ValidationError("Нельзя подписываться на самого себя.")

    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['user', 'author'],
        #         name='unique_subscription'
        #     )
        # ]

    # def __str__(self):
    #     return f'{self.user.username} подписан на {self.author.username}'


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(Announcement,
                                  on_delete=models.CASCADE)
    ad_receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    status = models.CharField(choices=STATUS_VALUES,
                              default='pending', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
        constraints = [
            models.UniqueConstraint(
                fields=['ad_sender', 'ad_receiver'],
                name='unique_ExchangeProposal'
            )
        ]

class category(models.Model):
    title = models.CharField(unique=True, verbose_name='Название', max_length=256)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
