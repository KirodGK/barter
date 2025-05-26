from django.contrib import admin

# Register your models here.
from .models import Announcement, ExchangeProposal, Category, Condition


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    pass

@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    pass
