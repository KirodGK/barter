from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db import models

from .validators import AnnouncementSerializer
from .models import Announcement
from .forms import AnnouncementForm



class AnnouncementViews(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementSerializer
    
    # @action(detail=False, methods=['POST'])
    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def view(self, request):
        form = AnnouncementForm
        context = {'form': form}
        return render(request, 'form.html', context)
    @action(detail=False, methods=['GET'])
    def listing(self, request):
        list = Announcement.objects.all()
        context = {'list': list}
        return render(request, 'list.html', context)
    
    @action(detail=True, methods=['GET'], url_path='details')
    def detail_view(self, request, pk=None):
        template_name = 'detail.html'
        announcement = get_object_or_404(Announcement, pk=pk)
        context = {
            'Announcement': announcement,
            'request': request  # <-- добавляем это!
        }
        return render(request, template_name, context)

    
