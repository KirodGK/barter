from django.contrib import admin

# Register your models here.
from .models import Announcement, ExchangeProposal


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    # list_display = ('id', "description", "category")
    
    # list_filter = ('id',)
    pass

@admin.register(ExchangeProposal)
class AnnouncementAdmin(admin.ModelAdmin):
    # list_display = ('id', "description", "category")
    
    # list_filter = ('id',)
    pass