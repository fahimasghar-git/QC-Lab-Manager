from django.contrib import admin
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q, F
from datetime import timedelta
import json

from unfold.admin import ModelAdmin

from .models import ReportGenerator
from django.contrib.auth import get_user_model
from resources.models import CompetencyRecord
from management.models import Document, NonConformance, InternalAudit
import csv
from django.http import HttpResponse
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


@admin.register(ReportGenerator)
class ReportGeneratorAdmin(ModelAdmin):
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

    def changelist_view(self, request, extra_context=None):
        User = get_user_model()
        users = User.objects.all()
        
        # Check if form was submitted
        module = request.GET.get('module')
        if not module:
            context = {
                **self.admin_site.each_context(request),
                "title": "On-Demand Filter Reports",
                "users": users,
            }
            return render(request, "admin/reports/reportgenerator/form.html", context)
            
        # Process Report
        user_id = request.GET.get('user')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        status = request.GET.get('status')
        export_csv = request.GET.get('export') == 'csv'

        records = []
        headers = []
        report_title = "Filtered Report"

        if module == 'test_results':
            qs = TestResult.objects.all().select_related('sample', 'parameter', 'analyst')
            if user_id: qs = qs.filter(analyst_id=user_id)
            if date_from: qs = qs.filter(tested_at__date__gte=date_from)
            if date_to: qs = qs.filter(tested_at__date__lte=date_to)
            if status: qs = qs.filter(status=status)
            
            headers = ['Sample ID', 'Parameter', 'Analyst', 'Result', 'Status', 'Date Tested']
            records = [[r.sample.sample_id if r.sample else 'N/A', r.parameter.name, r.analyst.username if r.analyst else 'N/A', f"{r.result_value} {r.unit}", r.get_status_display(), r.tested_at.strftime('%Y-%m-%d') if r.tested_at else 'N/A'] for r in qs]
            report_title = "Test Results Performance Report"

        elif module == 'competency':
            qs = CompetencyRecord.objects.all().select_related('analyst', 'test_method')
            if user_id: qs = qs.filter(analyst_id=user_id)
            if date_from: qs = qs.filter(authorization_date__gte=date_from)
            if date_to: qs = qs.filter(authorization_date__lte=date_to)
            if status: qs = qs.filter(status=status)

            headers = ['Analyst', 'Test Method', 'Authorized By', 'Status', 'Auth Date']
            records = [[r.analyst.username if r.analyst else 'N/A', r.test_method.name if r.test_method else 'N/A', r.authorized_by.username if r.authorized_by else 'N/A', r.get_status_display(), r.authorization_date.strftime('%Y-%m-%d') if r.authorization_date else 'N/A'] for r in qs]
            report_title = "Personnel Competency Report"

        elif module == 'documents':
            qs = Document.objects.all()
            if user_id: qs = qs.filter(Q(prepared_by_id=user_id) | Q(reviewed_by_id=user_id) | Q(approved_by_id=user_id))
            if date_from: qs = qs.filter(issue_date__gte=date_from)
            if date_to: qs = qs.filter(issue_date__lte=date_to)
            if status: qs = qs.filter(status=status)

            headers = ['Doc ID', 'Title', 'Rev', 'Status', 'Issue Date', 'Next Review']
            records = [[r.document_id, r.title, r.revision_number, r.get_status_display(), r.issue_date.strftime('%Y-%m-%d') if r.issue_date else 'N/A', r.next_review_date.strftime('%Y-%m-%d') if r.next_review_date else 'N/A'] for r in qs]
            report_title = "Document Control Report"
            
        elif module == 'samples':
            qs = Sample.objects.all()
            if user_id: qs = qs.filter(Q(received_by_id=user_id) | Q(verified_by_id=user_id))
            if date_from: qs = qs.filter(received_date__date__gte=date_from)
            if date_to: qs = qs.filter(received_date__date__lte=date_to)
            if status: qs = qs.filter(status=status)

            headers = ['Sample ID', 'Product', 'Client', 'Priority', 'Status', 'Received Date']
            records = [[r.sample_id, r.product_name, r.client.name if r.client else 'N/A', r.get_priority_display(), r.get_status_display(), r.received_date.strftime('%Y-%m-%d') if r.received_date else 'N/A'] for r in qs]
            report_title = "Sample Registration Report"
            
        elif module == 'nc':
            qs = NonConformance.objects.all()
            if user_id: qs = qs.filter(Q(reported_by_id=user_id) | Q(assigned_to_id=user_id))
            if date_from: qs = qs.filter(date_reported__gte=date_from)
            if date_to: qs = qs.filter(date_reported__lte=date_to)
            if status: qs = qs.filter(status=status)

            headers = ['NC ID', 'Description', 'Reported By', 'Assigned To', 'Status', 'Date']
            records = [[r.nc_id, r.description[:50], r.reported_by.username if r.reported_by else 'N/A', r.assigned_to.username if r.assigned_to else 'N/A', r.get_status_display(), r.date_reported.strftime('%Y-%m-%d') if r.date_reported else 'N/A'] for r in qs]
            report_title = "Non-Conformance (CAPA) Report"

        if export_csv:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{module}_report.csv"'
            writer = csv.writer(response)
            writer.writerow([report_title])
            writer.writerow(headers)
            writer.writerows(records)
            return response

        context = {
            "title": report_title,
            "headers": headers,
            "records": records,
            "date_from": date_from,
            "date_to": date_to,
            "user_filtered": User.objects.get(id=user_id).username if user_id else "All Users",
        }
        return render(request, "admin/reports/reportgenerator/print.html", context)
