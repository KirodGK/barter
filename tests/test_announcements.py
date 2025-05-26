import pytest
from django.urls import reverse
from api.models import Announcement

@pytest.mark.django_db
def test_listing_view_authenticated(client, user_sender):
    client.login(username='sender', password='pass')
    url = reverse('api:announcement-listing')
    response = client.get(url)
    assert response.status_code == 200
    assert 'list.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_create_announcement(client, user_sender, category, condition):
    client.login(username='sender', password='pass')
    url = reverse('api:announcement-create-announcement')
    response = client.post(url, {
        'title': 'Барабан',
        'description': 'Музыкальный инструмент',
        'category': category.id,
        'condition': condition.id
    })
    assert response.status_code == 302
    assert Announcement.objects.filter(title='Барабан').exists()

@pytest.mark.django_db
def test_delete_announcement_author_can_delete(client, user_receiver, announcement):
    client.login(username='receiver', password='pass')
    url = reverse('api:announcement-delete', kwargs={'pk': announcement.pk})
    response = client.post(url)

    assert response.status_code == 302
    assert not Announcement.objects.filter(pk=announcement.pk).exists()


@pytest.mark.django_db
def test_delete_announcement_not_author_cannot_delete(client, user_sender, announcement):
    client.login(username='sender', password='pass')
    url = reverse('api:announcement-delete', kwargs={'pk': announcement.pk})
    response = client.post(url)
    assert response.status_code == 200
    assert Announcement.objects.filter(pk=announcement.pk).exists()
    assert 'detail.html' in [t.name for t in response.templates]
    assert 'Нет прав на удаление' in response.content.decode('utf-8')
    
@pytest.mark.django_db
def test_detail_view(client, user_sender, announcement):
    client.login(username='sender', password='pass')
    url = reverse('api:announcement-detail-view', kwargs={'pk': announcement.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'detail.html' in [t.name for t in response.templates]
    
@pytest.mark.django_db
def test_filtered_list(client, user_sender, announcement):
    client.login(username='sender', password='pass')
    url = reverse('api:announcement-listing')
    response = client.get(url, {'q': 'лефон'})
    assert response.status_code == 200
    page_obj = response.context['page_obj']
    assert any(a.title == 'Телефон' for a in page_obj)
    response_empty = client.get(url, {'q': 'НеСуществующийТекст'})
    assert response_empty.status_code == 200
    page_obj_empty = response_empty.context['page_obj']
    assert len(page_obj_empty) == 0
