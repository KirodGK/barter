from site import USER_BASE
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



class Announcement(models.Model):
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='subscriber',
    #     verbose_name='Подписчик'
    # )
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='subscribing',
    #     verbose_name='Автор'
    # )
    title = models.TextField
    description = models.TextField
    image_ur = models.TextField(null=True)
    category = models.ForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.TextField(User, on_delete=models.CASCADE,
                              related_name='Автор',
                              verbose_name='Автор')
    item_condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.NEW,
    )

    # def clean(self):
    #     if self.user == self.author:
    #         raise ValidationError("Нельзя подписываться на самого себя.")

    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'