from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import TestBOM, BOMItem, InventoryIssuance

class BOMItemInline(TabularInline):
    model = BOMItem
    extra = 1
    autocomplete_fields = ['inventory_item']

@admin.register(TestBOM)
class TestBOMAdmin(ModelAdmin):
    list_display = ('parameter', 'estimated_cost', 'items_count')
    search_fields = ('parameter__name',)
    autocomplete_fields = ['parameter']
    inlines = [BOMItemInline]

    def estimated_cost(self, obj):
        return f"${obj.estimated_cost:.2f}"
    
    def items_count(self, obj):
        return obj.items.count()


@admin.register(InventoryIssuance)
class InventoryIssuanceAdmin(ModelAdmin):
    list_display = ('inventory_item', 'quantity_issued', 'calculated_cost', 'test_result', 'issued_by', 'issued_at')
    list_filter = ('issued_at', 'inventory_item', 'issued_by')
    search_fields = ('inventory_item__name', 'test_result__sample__sample_id', 'purpose')
    autocomplete_fields = ['inventory_item', 'test_result', 'issued_by']
    readonly_fields = ('calculated_cost', 'issued_at')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Cannot edit issuances once made to preserve stock integrity
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.issued_by = request.user
        super().save_model(request, obj, form, change)

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from .models import CostingDashboard
from resources.models import ReagentStandard

@admin.register(CostingDashboard)
class CostingDashboardAdmin(ModelAdmin):
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

    def changelist_view(self, request, extra_context=None):
        now = timezone.now()
        current_month = now.month
        current_year = now.year

        # Get all issuances for the current month
        issuances = InventoryIssuance.objects.filter(
            issued_at__year=current_year,
            issued_at__month=current_month
        ).select_related('inventory_item', 'test_result', 'test_result__parameter')

        total_cost = sum(i.calculated_cost for i in issuances)
        
        # Breakdown by parameter
        param_costs = {}
        for i in issuances:
            param_name = i.test_result.parameter.name if i.test_result else "General / Standard Prep"
            if param_name not in param_costs:
                param_costs[param_name] = 0
            param_costs[param_name] += i.calculated_cost

        # Sort by cost descending
        param_costs_sorted = sorted(param_costs.items(), key=lambda x: x[1], reverse=True)

        context = {
            **self.admin_site.each_context(request),
            "title": "Costing & Financial Reports",
            "current_month_name": now.strftime("%B %Y"),
            "total_cost": total_cost,
            "param_costs": param_costs_sorted,
            "issuances": issuances.order_by('-calculated_cost')[:50], # Top 50 expensive issuances
        }
        
        return render(request, "admin/inventory/costingdashboard/change_list.html", context)
