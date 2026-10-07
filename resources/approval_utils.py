from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib import admin, messages

class ISOApprovalModel(models.Model):
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_%(class)s', on_delete=models.SET_NULL, null=True, blank=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='checked_%(class)s', on_delete=models.SET_NULL, null=True, blank=True)
    checked_at = models.DateTimeField(null=True, blank=True)
    
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_%(class)s', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=[
        ('DRAFT', 'Draft'),
        ('PREPARED', 'Prepared / Submitted'),
        ('CHECKED', 'Checked / Reviewed'),
        ('APPROVED', 'Approved'),
    ], default='DRAFT')

    class Meta:
        abstract = True

def action_mark_prepared(modeladmin, request, queryset):
    for obj in queryset:
        obj.prepared_by = request.user
        obj.prepared_at = timezone.now()
        obj.status = 'PREPARED'
        obj.save()
    messages.success(request, f"Marked {queryset.count()} records as PREPARED.")
action_mark_prepared.short_description = "Sign as PREPARED (Action)"

def action_mark_checked(modeladmin, request, queryset):
    for obj in queryset:
        obj.checked_by = request.user
        obj.checked_at = timezone.now()
        if obj.status in ['DRAFT', 'PREPARED']:
            obj.status = 'CHECKED'
        obj.save()
    messages.success(request, f"Marked {queryset.count()} records as CHECKED.")
action_mark_checked.short_description = "Sign as CHECKED / REVIEWED (Action)"

def action_mark_approved(modeladmin, request, queryset):
    for obj in queryset:
        obj.approved_by = request.user
        obj.approved_at = timezone.now()
        obj.status = 'APPROVED'
        obj.save()
    messages.success(request, f"Marked {queryset.count()} records as APPROVED.")
action_mark_approved.short_description = "Sign as APPROVED (Action)"

