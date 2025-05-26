from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Announcement, Category, Condition, ExchangeProposal
from .forms import UserForm, AnnouncementForm, ExchangeProposalForm
from .serializers import AnnouncementSerializer, ExchangeProposalCreateSerializer
from barter_system.constant import STATUS_VALUES


class AnnouncementViews(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AnnouncementSerializer

    @action(detail=False, methods=['get'], url_path='list', permission_classes=[IsAuthenticated])
    def listing(self, request):
        if not request.user.is_authenticated:
            return redirect('/api/templates/errors/403.html', 403)

        queryset = Announcement.objects.all()
        search_query = request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        condition = request.GET.get('condition')
        if condition:
            queryset = queryset.filter(condition=condition)
        print(queryset.query)
        paginator = Paginator(queryset, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'search_query': search_query,
            'selected_category': category,
            'selected_condition': condition,
            'category_choices': Category.objects.all(),
            'condition_choices': Condition.objects.all(),
        }

        return render(request, 'list.html', context)

    @action(detail=True, methods=['get'], url_path='detail',
            permission_classes=[IsAuthenticated])
    def detail_view(self, request, pk=None):
        announcement = get_object_or_404(Announcement, pk=pk)
        return render(request, 'detail.html',
                      {'Announcement': announcement, 
                       'form': ExchangeProposalForm()})

    @action(detail=False, methods=['get', 'post'], url_path='register',
            permission_classes=[AllowAny])
    def register(self, request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/announcement/login/')
        else:
            form = UserForm()
        return render(request, 'register.html', {'form': form})

    @action(detail=False, methods=['get', 'post'], url_path='login',
            permission_classes=[AllowAny])
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
        return render(request, 'login.html', {'form': UserForm(),
                                              'error': error})

    @action(detail=False, methods=['get'], url_path='logout',
            permission_classes=[IsAuthenticated])
    def logout_view(self, request):
        logout(request)
        return redirect('/announcement/login/')

    @action(detail=False, methods=['get', 'post'], url_path='create',
            permission_classes=[IsAuthenticated])
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
            return redirect('api:announcement-listing')  # 302 редирект
        else:
            form = ExchangeProposalForm()  # для корректного рендера detail.html
            context = {
                'Announcement': announcement,
                'error': 'Нет прав на удаление',
                'form': form,
            }
            return render(request, 'detail.html', context)

    @action(detail=True, methods=['get', 'post'], url_path='edit',
            permission_classes=[IsAuthenticated])
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

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def create_exchange_proposal(self, request, pk=None):
        announcement = get_object_or_404(Announcement, pk=pk)
        serializer = ExchangeProposalCreateSerializer(
            data=request.data,
            context={'request': request, 'announcement': announcement}
        )
        if serializer.is_valid():
            serializer.save()
            return redirect('api:announcement-detail-view', pk=pk)
        else:
            form = ExchangeProposalForm(request.data)
            for field, errors in serializer.errors.items():
                if field == 'non_field_errors':
                    for error in errors:
                        form.add_error(None, error)
                else:
                    for error in errors:
                        form.add_error(field, error)

            return render(request, 'detail.html', {
                'Announcement': announcement,
                'form': form,
            })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_exchange_status(self, request, pk=None):
        proposal = get_object_or_404(ExchangeProposal, pk=pk,
                                     ad_receiver=request.user)
        new_status = request.POST.get('status')

        if new_status not in dict(STATUS_VALUES).keys():
            messages.error(request, 'Недопустимый статус')
            return redirect('api:announcement-listing-all-exchange-proposals')

        proposal.status = new_status
        proposal.save()
        return redirect('api:announcement-listing-all-exchange-proposals')

    def get_received_proposals(self, request):
        user = request.user
        proposals = ExchangeProposal.objects.filter(ad_receiver=user)

        filter_sender = request.GET.get('sender', '').strip()
        filter_status = request.GET.get('status_received', '')

        if filter_sender:
            proposals = proposals.filter(
                ad_sender__username__icontains=filter_sender)
        if filter_status:
            proposals = proposals.filter(status=filter_status)

        return proposals, filter_sender, filter_status

    def get_sent_proposals(self, request):
        user = request.user
        proposals = ExchangeProposal.objects.filter(ad_sender=user)

        filter_receiver = request.GET.get('receiver', '').strip()
        filter_status = request.GET.get('status_sent', '')

        if filter_receiver:
            proposals = proposals.filter(
                ad_receiver__username__icontains=filter_receiver)
        if filter_status:
            proposals = proposals.filter(status=filter_status)

        return proposals, filter_receiver, filter_status

    @action(detail=False, methods=['get'], url_path='proposal',
            permission_classes=[IsAuthenticated])
    def listing_all_exchange_proposals(self, request):
        (received_proposals, filter_sender,
         filter_status_received) = self.get_received_proposals(request)
        (sent_proposals, filter_receiver,
         filter_status_sent) = self.get_sent_proposals(request)

        return render(request, 'exchange_proposals_list.html', {
            'received_proposals': received_proposals,
            'sent_proposals': sent_proposals,
            'filter_sender': filter_sender,
            'filter_status_received': filter_status_received,
            'filter_receiver': filter_receiver,
            'filter_status_sent': filter_status_sent,
            'status_choices': STATUS_VALUES,
        })
