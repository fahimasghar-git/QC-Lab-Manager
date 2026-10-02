import re

admin_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(admin_path, 'r') as f:
    content = f.read()

old_pr_admin = """@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('id', 'item_description', 'supplier', 'status', 'requested_by', 'requested_date')
    list_filter = ('status', 'supplier')"""

new_pr_admin = """@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('id', 'item_description', 'quantity_required', 'status', 'requested_by', 'requested_date')
    list_filter = ('status', 'supplier')
    search_fields = ('item_description', 'specification', 'purpose')
    actions = ['print_purchase_demand']

    fieldsets = (
        ('Request Details', {
            'fields': ('item_description', 'specification', 'purpose')
        }),
        ('Quantities', {
            'fields': ('quantity_required', 'stock_in_hand')
        }),
        ('Status & Approval', {
            'fields': ('supplier', 'status', 'requested_by', 'approved_by')
        }),
    )

    @admin.action(description='🖨️ Print Store Purchase Demand (QCL-FRM-6.07)')
    def print_purchase_demand(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/store_purchase_demand.html', {'requests': queryset})
"""

content = content.replace(old_pr_admin, new_pr_admin)

with open(admin_path, 'w') as f:
    f.write(content)
print("Updated PR admin.")
