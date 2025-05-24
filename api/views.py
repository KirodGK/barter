from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

from .models import Announcement
from .forms import UserForm, AnnouncementForm
from .serializers import AnnouncementSerializer

class AnnouncementViews(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementSerializer

    # @action(detail=False, methods=['get'], url_path='list', permission_classes=[AllowAny])
    # def listing(self, request):
    #     announcements = Announcement.objects.all()
    #     paginator = Paginator(announcements, 8)  # по 8 на страницу
    #     page_number = request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #     return render(request, 'list.html', {'page_obj': page_obj})
    @action(detail=False, methods=['get'], url_path='list', permission_classes=[AllowAny])
    def listing(self, request):
        queryset = Announcement.objects.all()

        # 🔍 Поиск по ключевым словам
        search_query = request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # 🔽 Фильтрация по категории
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # 🔘 Фильтрация по состоянию
        condition = request.GET.get('condition')
        if condition:
            queryset = queryset.filter(condition=condition)

        paginator = Paginator(queryset, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Передадим фильтры обратно в шаблон
        context = {
            'page_obj': page_obj,
            'search_query': search_query,
            'selected_category': category,
            'selected_condition': condition,
        }

        return render(request, 'list.html', context)
    @action(detail=True, methods=['get'], url_path='detail', permission_classes=[AllowAny])
    def detail_view(self, request, pk=None):
        announcement = get_object_or_404(Announcement, pk=pk)
        return render(request, 'detail.html', {'Announcement': announcement})

    @action(detail=False, methods=['get', 'post'], url_path='register', permission_classes=[AllowAny])
    def register(self, request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/announcement/login/')
        else:
            form = UserForm()
        return render(request, 'register.html', {'form': form})

    @action(detail=False, methods=['get', 'post'], url_path='login', permission_classes=[AllowAny])
    def login_view(self, request):
        error = None
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/announcement/list/')
            else:
                error = 'Неверные имя пользователя или пароль'
        return render(request, 'login.html', {'form': UserForm(), 'error': error})
    
    @action(detail=False, methods=['get'], url_path='logout', permission_classes=[IsAuthenticated])
    def logout_view(self, request):
        logout(request)
        return redirect('/announcement/login/')
    
    @action(detail=False, methods=['get', 'post'], url_path='create', permission_classes=[IsAuthenticated])
    def create_announcement(self, request):
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)
            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.author = request.user
                announcement.save()
                return redirect('api:announcement-listing')
        else:
            form = AnnouncementForm()
        return render(request, 'announcement_form.html', {
            'form': form,
            'title': 'Создание объявления',
            'button_label': 'Создать'
        })
    
    @action(detail=True, methods=['post'], url_path='delete', permission_classes=[IsAuthenticated])
    def delete(self, request, pk=None):
        
        announcement = get_object_or_404(Announcement, pk=pk)
        user = request.user

        if user == announcement.author:
            announcement.delete()
            print(f"Announcement {pk} deleted by user {user}")
            return redirect('api:announcement-listing')
        else:
            announcement = get_object_or_404(Announcement, pk=pk)
            context = {'Announcement': announcement, 'error': 'Нет прав на удаление'}
            return render(request, 'detail.html', context)
        
    @action(detail=True, methods=['get', 'post'], url_path='edit', permission_classes=[IsAuthenticated])
    def edit_announcement(self, request, pk=None):
        announcement = get_object_or_404(Announcement, pk=pk)

        if announcement.author != request.user:
            return render(request, 'detail.html', {
                'Announcement': announcement,
                'error': 'Нет прав на редактирование'
            })

        if request.method == 'POST':
            form = AnnouncementForm(request.POST, instance=announcement)
            if form.is_valid():
                form.save()
                return redirect('api:announcement-detail-view', pk=pk)
        else:
            form = AnnouncementForm(instance=announcement)

        return render(request, 'announcement_form.html', {
            'form': form,
            'title': 'Редактирование объявления',
            'button_label': 'Сохранить изменения'
        })
