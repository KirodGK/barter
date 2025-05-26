import pytest
from django.urls import reverse
from api.models import ExchangeProposal

@pytest.mark.django_db
def test_create_exchange_proposal(client, user_sender, announcement):
    client.login(username='sender', password='pass')
    url = reverse('api:announcement-create-exchange-proposal', kwargs={'pk': announcement.pk})
    data = {'comment': 'Хочу обменяться на мой планшет'}
    response = client.post(url, data)
    assert response.status_code == 302
    proposal = ExchangeProposal.objects.filter(ad_sender=user_sender, announcement=announcement).first()
    assert proposal is not None
    assert proposal.comment == data['comment']
    assert proposal.status == 'pending'

@pytest.mark.django_db
def test_change_exchange_status(client, user_receiver, user_sender, announcement):
    proposal = ExchangeProposal.objects.create(
        announcement=announcement,
        ad_sender=user_sender,
        ad_receiver=user_receiver,
        comment='Обмен',
        status='pending'
    )
    client.login(username='receiver', password='pass')
    url = reverse('api:announcement-change-exchange-status', kwargs={'pk': proposal.pk})
    new_status = 'accepted'
    response = client.post(url, {'status': new_status})
    assert response.status_code == 302
    proposal.refresh_from_db()
    assert proposal.status == new_status

@pytest.mark.django_db
def test_listing_all_exchange_proposals_filters(client, user_sender, user_receiver, announcement):
    ExchangeProposal.objects.create(
        announcement=announcement,
        ad_sender=user_sender,
        ad_receiver=user_receiver,
        comment='Первое предложение',
        status='pending'
    )
    ExchangeProposal.objects.create(
        announcement=announcement,
        ad_sender=user_receiver,
        ad_receiver=user_sender,
        comment='Ответное предложение',
        status='accepted'
    )
    client.login(username='receiver', password='pass')
    url = reverse('api:announcement-listing-all-exchange-proposals')

    response = client.get(url, {'sender': 'sender'})
    assert response.status_code == 200
    assert 'Первое предложение' in response.content.decode()

    response = client.get(url, {'status_received': 'pending'})
    assert response.status_code == 200
    assert 'Первое предложение' in response.content.decode()

    response = client.get(url, {'receiver': 'sender'})
    assert response.status_code == 200
    assert 'Ответное предложение' in response.content.decode()

    response = client.get(url, {'status_sent': 'accepted'})
    assert response.status_code == 200
    assert 'Ответное предложение' in response.content.decode()