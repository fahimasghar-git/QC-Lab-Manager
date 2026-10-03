from django.db import models
from samples.models import Sample
from testing.models import TestResult

class PendingApproval(Sample):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'Pending QCM Approval'
        verbose_name_plural = 'Pending QCM Approvals'

class PendingVerification(Sample):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'Pending AQCM Review'
        verbose_name_plural = 'Pending AQCM Reviews'

class MyAssignedTest(TestResult):
    class Meta:
        proxy = True
        app_label = 'inbox'
        verbose_name = 'My Assigned Test'
        verbose_name_plural = 'My Assigned Tests'
