import re

admin_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(admin_path, 'r') as f:
    content = f.read()

# 1. CompetencyRecord
old_cr = """        ('Authorization', {
            'fields': ('status', 'authorized_by', 'notes')
        }),"""
new_cr = """        ('Authorization & Signatures', {
            'fields': ('status', 'authorized_by', 'notes', 'prepared_by', 'checked_by', 'approved_by')
        }),"""
content = content.replace(old_cr, new_cr)

# 2. CompetencyEvaluation
old_ce = """        ('Approval & Remarks', {
            'fields': ('remarks',)
        }),"""
new_ce = """        ('Approval & Remarks', {
            'fields': ('remarks', 'manager_qc')
        }),"""
content = content.replace(old_ce, new_ce)

# 3. Equipment
old_eq = """        ('Status & Validation', {
            'fields': ('status', 'date_put_into_service')
        }),"""
new_eq = """        ('Status & Validation', {
            'fields': ('status', 'date_put_into_service', 'prepared_by', 'reviewed_by', 'approved_by')
        }),"""
content = content.replace(old_eq, new_eq)

# 4. EquipmentMaintenance
if "fieldsets =" not in content.split("class EquipmentMaintenanceAdmin")[1]:
    old_em = """    search_fields = ('equipment__name', 'equipment__identification_no', 'maintenance_by')
    actions = ['print_maintenance_record']"""
    
    new_em = """    search_fields = ('equipment__name', 'equipment__identification_no', 'maintenance_by')
    actions = ['print_maintenance_record']
    
    fieldsets = (
        ('Maintenance Details', {
            'fields': ('equipment', 'maintenance_date', 'parts_repaired_replaced', 'maintenance_by', 'remarks')
        }),
        ('Signatures', {
            'fields': ('prepared_by', 'reviewed_by', 'approved_by')
        }),
    )"""
    content = content.replace(old_em, new_em)

# 5. PurchaseRequest
old_pr = """        ('Status & Approval', {
            'fields': ('supplier', 'status', 'requested_by', 'approved_by')
        }),"""
new_pr = """        ('Document Control', {
            'fields': ('spd_no', 'insp_mints_no', 'service_call_no')
        }),
        ('Status & Signatures', {
            'fields': ('supplier', 'status', 'requested_by', 'store_keeper', 'approved_by')
        }),"""
content = content.replace(old_pr, new_pr)

with open(admin_path, 'w') as f:
    f.write(content)
print("Updated admin.py fieldsets.")
