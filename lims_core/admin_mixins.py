from django.utils import timezone
from django.contrib import admin
from django.contrib import messages

class DigitalSignatureMixin:
    def get_readonly_fields(self, request, obj=None):
        ro_fields = super().get_readonly_fields(request, obj) or []
        signature_fields = [
            'prepared_by', 'prepared_at', 
            'reviewed_by', 'reviewed_at', 'checked_by', 'checked_at',
            'approved_by', 'approved_at', 'authorized_by', 'authorized_at',
            'verified_by', 'verified_at', 'performed_by', 'performed_at',
            'status'
        ]
        return list(ro_fields) + [f for f in signature_fields if hasattr(self.model, f)]

    def has_role(self, user, allowed_roles):
        if user.is_superuser:
            return True
        user_groups = user.groups.values_list('name', flat=True)
        return any(role in user_groups for role in allowed_roles)

    @admin.action(description="🖋️ Submit / Sign as Preparer (Analyst/AQCM)")
    def action_sign_prepared(self, request, queryset):
        if not self.has_role(request.user, ['Analyst', 'AQCM', 'QCM']):
            self.message_user(request, "Permission Denied: You must be an Analyst, AQCM, or QCM to prepare documents.", level=messages.ERROR)
            return

        count = 0
        for obj in queryset:
            if hasattr(obj, 'prepared_by') and hasattr(obj, 'prepared_at'):
                obj.prepared_by = request.user
                obj.prepared_at = timezone.now()
                if hasattr(obj, 'status'):
                    if hasattr(obj, "status"): obj.status ='PENDING_REVIEW'
                obj.save()
                count += 1
            elif hasattr(obj, 'performed_by') and hasattr(obj, 'performed_at'):
                obj.performed_by = request.user
                obj.performed_at = timezone.now()
                if hasattr(obj, 'status'):
                    if hasattr(obj, "status"): obj.status ='PENDING_VERIFICATION'
                obj.save()
                count += 1
        self.message_user(request, f"{count} documents digitally signed as Prepared/Performed.", messages.SUCCESS)

    @admin.action(description="🖋️ Sign as Reviewer/Checker (AQCM/QCM)")
    def action_sign_reviewed(self, request, queryset):
        if not self.has_role(request.user, ['AQCM', 'QCM']):
            self.message_user(request, "Permission Denied: You must be an AQCM or QCM to review documents.", level=messages.ERROR)
            return

        count = 0
        for obj in queryset:
            if hasattr(obj, 'reviewed_by') and hasattr(obj, 'reviewed_at'):
                obj.reviewed_by = request.user
                obj.reviewed_at = timezone.now()
                if hasattr(obj, 'status'):
                    if hasattr(obj, "status"): obj.status ='PENDING_APPROVAL'
                obj.save()
                count += 1
            elif hasattr(obj, 'checked_by') and hasattr(obj, 'checked_at'):
                obj.checked_by = request.user
                obj.checked_at = timezone.now()
                if hasattr(obj, 'status'):
                    if hasattr(obj, "status"): obj.status ='PENDING_APPROVAL'
                obj.save()
                count += 1
            elif hasattr(obj, 'verified_by') and hasattr(obj, 'verified_at'):
                obj.verified_by = request.user
                obj.verified_at = timezone.now()
                if hasattr(obj, 'status'):
                    if hasattr(obj, "status"): obj.status ='APPROVED'
                obj.save()
                count += 1
        self.message_user(request, f"{count} documents digitally signed as Reviewed/Verified.", messages.SUCCESS)

    @admin.action(description="🖋️ Approve Document (QCM/CEO)")
    def action_sign_approved(self, request, queryset):
        if not self.has_role(request.user, ['QCM', 'CEO']):
            self.message_user(request, "Permission Denied: You must be a QCM or CEO to approve documents.", level=messages.ERROR)
            return

        count = 0
        for obj in queryset:
            if hasattr(obj, 'approved_by') and hasattr(obj, 'approved_at'):
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
                if hasattr(obj, 'status'):
                    if hasattr(obj, "status"): obj.status ='APPROVED'
                obj.save()
                count += 1
            elif hasattr(obj, 'authorized_by') and hasattr(obj, 'authorized_at'):
                obj.authorized_by = request.user
                obj.authorized_at = timezone.now()
                if hasattr(obj, 'status'):
                    if hasattr(obj, "status"): obj.status ='APPROVED'
                obj.save()
                count += 1
        self.message_user(request, f"{count} documents digitally approved.", messages.SUCCESS)
        
    def get_actions(self, request):
        actions = super().get_actions(request)
        if hasattr(self.model, 'prepared_by') or hasattr(self.model, 'performed_by'):
            actions['action_sign_prepared'] = (self.action_sign_prepared, 'action_sign_prepared', "🖋️ Submit / Sign as Preparer (Analyst/AQCM)")
        if hasattr(self.model, 'reviewed_by') or hasattr(self.model, 'checked_by') or hasattr(self.model, 'verified_by'):
            actions['action_sign_reviewed'] = (self.action_sign_reviewed, 'action_sign_reviewed', "🖋️ Sign as Reviewer/Checker (AQCM/QCM)")
        if hasattr(self.model, 'approved_by') or hasattr(self.model, 'authorized_by'):
            actions['action_sign_approved'] = (self.action_sign_approved, 'action_sign_approved', "🖋️ Approve Document (QCM/CEO)")
        return actions
