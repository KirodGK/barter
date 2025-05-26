import pytest
from django.contrib.auth.models import User
from api.models import Category, Condition, Announcement

@pytest.fixture
def user_sender(db):
    return User.objects.create_user(username='sender', password='pass')

@pytest.fixture
def user_receiver(db):
    return User.objects.create_user(username='receiver', password='pass')

@pytest.fixture
def category(db):
    return Category.objects.create(title='Электроника')

@pytest.fixture
def condition(db):
    return Condition.objects.create(title='Новое')

@pytest.fixture
def announcement(user_receiver, category, condition):
    return Announcement.objects.create(
        title='Телефон',
        description='Описание телефона',
        author=user_receiver,
        category=category,
        condition=condition
    )