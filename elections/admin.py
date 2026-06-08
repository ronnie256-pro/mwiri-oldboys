from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ElectionCategory, Position, Candidate

@admin.register(ElectionCategory)
class ElectionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'category__name')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'status', 'created_at')
    list_filter = ('status', 'position__category', 'position')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'position__title')
    actions = ['approve_candidates', 'deny_candidates']

    @admin.action(description=_("Approve selected candidates"))
    def approve_candidates(self, request, queryset):
        updated_count = queryset.update(status=Candidate.STATUS_APPROVED)
        self.message_user(request, _(f"{updated_count} candidates were successfully approved."))

    @admin.action(description=_("Deny selected candidates"))
    def deny_candidates(self, request, queryset):
        updated_count = queryset.update(status=Candidate.STATUS_DENIED)
        self.message_user(request, _(f"{updated_count} candidates were successfully denied."))
