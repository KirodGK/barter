from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers


from .models import Announcement, ExchangeProposal

User = get_user_model()


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'image_ur', 'category', 'condition']

    def create(self, validated_data):
        request = self.context.get('request')
        return Announcement.objects.create(
            author=request.user, **validated_data)