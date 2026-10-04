from django.contrib import admin
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q, F
from datetime import timedelta
import json

from unfold.admin import ModelAdmin
from .models import PerformanceMetrics
from testing.models import TestResult, Parameter
from samples.models import Sample

@admin.register(PerformanceMetrics)
class PerformanceMetricsAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        now = timezone.now()
        current_month = now.month
        current_year = now.year

        # 1. Total tests done in the current month (status='VERIFIED' or Sample is 'APPROVED')
        # We'll use tested_at month
        completed_tests = TestResult.objects.filter(
            tested_at__year=current_year,
            tested_at__month=current_month,
            status__in=['VERIFIED', 'PENDING_VERIFICATION'] # Assuming if it's tested, it's completed by analyst
        )
        total_tests_done = completed_tests.count()

        # 2. Parameter tested frequency
        parameter_stats = list(completed_tests.values('parameter__name').annotate(count=Count('id')).order_by('-count'))

        # 3. Analyst performance
        analyst_stats = list(completed_tests.values('analyst__username').annotate(count=Count('id')).order_by('-count'))

        # 4. Analyst x Parameter
        analyst_param_stats = list(completed_tests.values('analyst__username', 'parameter__name').annotate(count=Count('id')).order_by('analyst__username', '-count'))

        # 5. Completion rate (All tests assigned this month vs completed)
        assigned_this_month = TestResult.objects.filter(sample__received_date__year=current_year, sample__received_date__month=current_month).exclude(result_type='BLANK').exclude(result_type='CRM')
        total_assigned = assigned_this_month.count()
        completed_this_month = assigned_this_month.filter(status='VERIFIED').count()
        completion_rate = round((completed_this_month / total_assigned * 100), 2) if total_assigned > 0 else 0

        # 6. In-time completion rate (Samples completed on or before due date)
        # Only look at Approved samples this month
        approved_samples = Sample.objects.filter(approved_at__year=current_year, approved_at__month=current_month, status='APPROVED')
        total_approved = approved_samples.count()
        
        in_time_samples = 0
        for s in approved_samples:
            if s.due_date and s.approved_at:
                # approved_at is datetime, due_date is date
                if s.approved_at.date() <= s.due_date:
                    in_time_samples += 1
            else:
                # If no due date, count it as in-time
                in_time_samples += 1
                
        in_time_rate = round((in_time_samples / total_approved * 100), 2) if total_approved > 0 else 0

        context = {
            **self.admin_site.each_context(request),
            "title": "Laboratory MIS Dashboard",
            "current_month_name": now.strftime("%B %Y"),
            "total_tests_done": total_tests_done,
            "parameter_stats": parameter_stats,
            "analyst_stats": analyst_stats,
            "analyst_param_stats": analyst_param_stats,
            "completion_rate": completion_rate,
            "in_time_rate": in_time_rate,
            "total_assigned": total_assigned,
            "completed_this_month": completed_this_month,
            "total_approved": total_approved,
            "in_time_samples": in_time_samples,
            # JSON versions for Chart.js
            "chart_labels_params": json.dumps([p['parameter__name'] for p in parameter_stats]),
            "chart_data_params": json.dumps([p['count'] for p in parameter_stats]),
            "chart_labels_analysts": json.dumps([a['analyst__username'] or 'Unassigned' for a in analyst_stats]),
            "chart_data_analysts": json.dumps([a['count'] for a in analyst_stats]),
        }
        
        return render(request, "admin/reports/performancemetrics/change_list.html", context)
