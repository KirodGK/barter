from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers


from .models import Announcement, ExchangeProposal

User = get_user_model()


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'image_url', 'category', 'condition']

    def create(self, validated_data):
        request = self.context.get('request')
        return Announcement.objects.create(
            author=request.user, **validated_data)
        
        
        
        
class ExchangeProposalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = ['comment']  # пользователь заполняет только комментарий

    def validate(self, attrs):
        request = self.context['request']
        announcement = self.context['announcement']

        if announcement.author == request.user:
            raise serializers.ValidationError("Нельзя создать предложение на собственное объявление.")

        # Проверяем, есть ли уже предложение от этого пользователя к данному объявлению
        if ExchangeProposal.objects.filter(
            announcement=announcement,
            ad_sender=request.user
        ).exists():
            raise serializers.ValidationError("Вы уже отправили предложение для этого объявления.")

        return attrs

    def create(self, validated_data):
        request = self.context['request']
        announcement = self.context['announcement']

        return ExchangeProposal.objects.create(
            announcement=announcement,
            ad_sender=request.user,
            ad_receiver=announcement.author,
            comment=validated_data['comment']
        )