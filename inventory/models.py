from django.db import models
from django.conf import settings
from testing.models import Parameter, TestResult
from resources.models import ReagentStandard
from django.core.exceptions import ValidationError

class TestBOM(models.Model):
    """Bill of Materials / Cost Recipe for a Test Parameter"""
    parameter = models.OneToOneField(Parameter, on_delete=models.CASCADE, related_name='bom')
    description = models.TextField(blank=True, null=True, help_text="Notes on this recipe")

    def __str__(self):
        return f"BOM/Recipe: {self.parameter.name}"

    @property
    def estimated_cost(self):
        return sum([item.total_cost for item in self.items.all()])

    class Meta:
        verbose_name = "Test Recipe / BOM"
        verbose_name_plural = "Test Recipes / BOMs"

class BOMItem(models.Model):
    bom = models.ForeignKey(TestBOM, on_delete=models.CASCADE, related_name='items')
    inventory_item = models.ForeignKey(ReagentStandard, on_delete=models.RESTRICT)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=4, help_text="Quantity required per test")

    def __str__(self):
        return f"{self.quantity_required} {self.inventory_item.unit_of_measure} of {self.inventory_item.name}"

    @property
    def total_cost(self):
        if self.inventory_item and self.inventory_item.unit_cost and self.quantity_required:
            return self.inventory_item.unit_cost * self.quantity_required
        return 0

class InventoryIssuance(models.Model):
    inventory_item = models.ForeignKey(ReagentStandard, on_delete=models.RESTRICT, related_name='issuances')
    test_result = models.ForeignKey(TestResult, on_delete=models.SET_NULL, null=True, blank=True, related_name='chemical_issuances', help_text="The specific test serial number this was issued for")
    
    quantity_issued = models.DecimalField(max_digits=10, decimal_places=4)
    calculated_cost = models.DecimalField(max_digits=10, decimal_places=4, editable=False, help_text="Automatically calculated at time of issuance")
    
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    issued_at = models.DateTimeField(auto_now_add=True)
    
    purpose = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Standard Preparation, Direct Testing")

    def clean(self):
        if self.pk is None:  # Only check on creation
            if self.inventory_item.current_stock < self.quantity_issued:
                raise ValidationError(f"Insufficient stock for {self.inventory_item.name}. Current stock: {self.inventory_item.current_stock}")

    def save(self, *args, **kwargs):
        if self.pk is None:
            # 1. Calculate historical cost at this exact moment
            self.calculated_cost = self.inventory_item.unit_cost * self.quantity_issued
            # 2. Deduct from stock
            self.inventory_item.current_stock -= self.quantity_issued
            self.inventory_item.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Refund stock on deletion
        self.inventory_item.current_stock += self.quantity_issued
        self.inventory_item.save()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Chemical/CRM Issuance Log"
        verbose_name_plural = "Chemical/CRM Issuance Logs"
        ordering = ['-issued_at']

    def __str__(self):
        return f"Issued {self.quantity_issued} of {self.inventory_item.name} for {self.test_result}"


class CostingDashboard(models.Model):
    class Meta:
        managed = False
        verbose_name = "Costing & Financial Reports"
        verbose_name_plural = "Costing & Financial Reports"
