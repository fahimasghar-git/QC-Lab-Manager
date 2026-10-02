import re

admin_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(admin_path, 'r') as f:
    content = f.read()

# Replace existing EquipmentAdmin
old_equip_admin = """@admin.register(Equipment)
class EquipmentAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('name', 'serial_number', 'status', 'location')
    list_filter = ('status', 'location')
    search_fields = ('name', 'serial_number', 'manufacturer')"""

new_equip_admin = """@admin.register(Equipment)
class EquipmentAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('name', 'identification_no', 'serial_number', 'status', 'location', 'calibration_frequency')
    list_filter = ('status', 'location', 'calibration_frequency')
    search_fields = ('name', 'identification_no', 'serial_number')
    actions = ['print_master_list', 'print_calibration_program']

    @admin.action(description='🖨️ Print Master List of Equipments (QCL-FRM-4.02)')
    def print_master_list(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/equipment_master_list.html', {'equipments': queryset})

    @admin.action(description='🖨️ Print Calibration Program (QCL-FRM-4.04)')
    def print_calibration_program(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/calibration_program.html', {'equipments': queryset})
"""

if old_equip_admin in content:
    content = content.replace(old_equip_admin, new_equip_admin)
else:
    # Use regex if spacing differs
    content = re.sub(r'@admin\.register\(Equipment\)\nclass EquipmentAdmin\(.*?\):.*?search_fields = \(.*?\)', new_equip_admin, content, flags=re.DOTALL)

# Add EquipmentMaintenanceAdmin
maintenance_admin = """
@admin.register(EquipmentMaintenance)
class EquipmentMaintenanceAdmin(ModelAdmin):
    list_display = ('equipment', 'maintenance_date', 'maintenance_by')
    list_filter = ('maintenance_date', 'equipment')
    search_fields = ('equipment__name', 'equipment__identification_no', 'maintenance_by')
    actions = ['print_maintenance_record']

    @admin.action(description='🖨️ Print Equipment Maintenance Record (QCL-FRM-4.03)')
    def print_maintenance_record(self, request, queryset):
        from django.shortcuts import render
        return render(request, 'resources/equipment_maintenance_record.html', {'maintenances': queryset})
"""
if "@admin.register(EquipmentMaintenance)" not in content:
    content += maintenance_admin

with open(admin_path, 'w') as f:
    f.write(content)

print("Equipment Admins Updated")
