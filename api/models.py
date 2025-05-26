from django.db import models
from django.contrib.auth.models import User

from barter_system.constant import (STATUS_VALUES,
                                    MAX_LENGTH_TITLE,
                                    MAX_LENGTH_COMMENT,
                                    MAX_LENGTH_STATUS)


class Category(models.Model):
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Condition(models.Model):
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Состояние'
        verbose_name_plural = 'Состояния'

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.TextField(verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image_url = models.TextField(
        null=True,
        blank=True,
        verbose_name='Ссылка на изображение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=1,
        verbose_name='Категория'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.ForeignKey(
        Condition,
        on_delete=models.SET_DEFAULT,
        default=1,
        verbose_name='Состояние'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f'Название: {self.title}, Автор: {self.author}'


class ExchangeProposal(models.Model):
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        related_name='proposals',
        verbose_name='Объявление'
    )
    ad_sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='exchangeproposals_sent'
    )
    ad_receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='exchangeproposals_received'
    )
    comment = models.CharField(
        max_length=MAX_LENGTH_COMMENT,
        verbose_name='Комментарий'
    )
    status = models.CharField(
        max_length=MAX_LENGTH_STATUS,
        choices=STATUS_VALUES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self):
        return (
            f'Товар: {self.announcement}, '
            f'Отправитель: {self.ad_sender}, '
            f'Получатель: {self.ad_receiver}'
        )
