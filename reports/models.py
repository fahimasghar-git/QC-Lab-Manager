from django.db import models

class PerformanceMetrics(models.Model):
    # Dummy model for routing the MIS report
    class Meta:
        managed = False
        verbose_name = "Laboratory KPI Dashboard"
        verbose_name_plural = "Laboratory KPI Dashboard"

class ReportGenerator(models.Model):
    class Meta:
        managed = False
        verbose_name = "On-Demand Filter Reports"
        verbose_name_plural = "On-Demand Filter Reports"
