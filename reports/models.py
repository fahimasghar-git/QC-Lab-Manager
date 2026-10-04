from django.db import models

class PerformanceMetrics(models.Model):
    # Dummy model for routing the MIS report
    class Meta:
        managed = False
        verbose_name = "Laboratory KPI Dashboard"
        verbose_name_plural = "Laboratory KPI Dashboard"
