import os
import re

models_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(models_path, 'r') as f:
    content = f.read()

# 1. Update Equipment Model
new_equip = """class Equipment(models.Model):
    history = HistoricalRecords()

    STATUS_CHOICES = [
        ('ACTIVE', 'Active / In Use'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('OUT_OF_SERVICE', 'Out of Service (Do Not Use)'),
        ('DECOMMISSIONED', 'Decommissioned'),
    ]

    name = models.CharField(max_length=150, help_text="e.g., Analytical Balance, UV-Vis Spectrophotometer")
    identification_no = models.CharField(max_length=50, blank=True, null=True, help_text="Internal ID e.g., EQ-01")
    manufacturer = models.CharField(max_length=150, blank=True, null=True)
    model_number = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, unique=True)
    
    operating_range = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 0-200g, 190-1100nm")
    location = models.CharField(max_length=100, help_text="Where is the equipment located?", blank=True, null=True)
    
    date_received = models.DateField(blank=True, null=True)
    date_put_into_service = models.DateField(blank=True, null=True)
    
    calibration_frequency = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Annually, 6 Months")
    maintenance_frequency = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Weekly, Monthly")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    class Meta:
        verbose_name = 'Equipment (QCL-FRM-4.02)'
        verbose_name_plural = 'Equipments (QCL-FRM-4.02)'

    def __str__(self):
        return f"{self.name} ({self.identification_no or self.serial_number})"
"""

content = re.sub(r'class Equipment\(models\.Model\):.*?def __str__\(self\):\n.*?return .*?\n', new_equip, content, flags=re.DOTALL)

# 2. Add EquipmentMaintenance Model below CalibrationRecord
new_maintenance = """
class EquipmentMaintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenances')
    maintenance_date = models.DateField()
    
    parts_repaired_replaced = models.CharField(max_length=255, blank=True, null=True, help_text="If any")
    maintenance_by = models.CharField(max_length=100, help_text="Who performed the maintenance?")
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Maintenance Record (QCL-FRM-4.03)'
        verbose_name_plural = 'Maintenance Records (QCL-FRM-4.03)'

    def __str__(self):
        return f"Maintenance: {self.equipment.name} on {self.maintenance_date}"
"""

content = content.replace("class CompetencyRecord(models.Model):", new_maintenance + "\nclass CompetencyRecord(models.Model):")

with open(models_path, 'w') as f:
    f.write(content)

print("Equipment models updated.")
