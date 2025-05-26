import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_register_view(client):
    url = reverse('api:announcement-register')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_view(client, user_sender):
    url = reverse('api:announcement-login-view')
    response = client.post(url, {'username': 'sender', 'password': 'pass'})
    assert response.status_code == 302
    assert response.url == '/announcement/list/'

@pytest.mark.django_db
def test_logout_view(client, user_sender):
    client.login(username='sender', password='pass')
    url = reverse('api:announcement-logout-view')
    response = client.get(url)
    assert response.status_code == 302
