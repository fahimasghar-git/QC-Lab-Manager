import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

old_supp = """class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # QCL-FRM-6.03 Fields"""

new_supp = """class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    requirements_from_supplier = models.TextField(blank=True, null=True, help_text="Range of products/services required")
    
    # --- QCL-FRM-6.01 Selection Criteria ---
    # General
    crit_1_registered = models.BooleanField(default=False, verbose_name="Supplier is legally registered")
    crit_1_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    crit_2_market_1yr = models.BooleanField(default=False, verbose_name="At least 1 year in market")
    crit_2_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    crit_3_offers_range = models.BooleanField(default=False, verbose_name="Offers required range of products/services")
    crit_3_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # Equipment
    crit_4_equipment_docs = models.BooleanField(default=False, verbose_name="Fulfills tech specs & provides docs (manuals/training)")
    crit_4_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # Calibration
    crit_5_calibration_traceability = models.BooleanField(default=False, verbose_name="Capability for traceability, uncertainty, range")
    crit_5_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    crit_6_iso17025 = models.BooleanField(default=False, verbose_name="Accredited on ISO/IEC 17025")
    crit_6_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # PT Services
    crit_7_iso17043 = models.BooleanField(default=False, verbose_name="Accredited for PT services (ISO/IEC 17043)")
    crit_7_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # Training
    crit_8_training_exp = models.BooleanField(default=False, verbose_name="Experience & Qualification of Trainers (PNAC preferred)")
    crit_8_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # Chemicals
    crit_9_msds = models.BooleanField(default=False, verbose_name="Provides supporting docs / MSDS")
    crit_9_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # CRM
    crit_10_crm_coa = models.BooleanField(default=False, verbose_name="Provides CoA & uncertainty (ISO/IEC 17034 certified)")
    crit_10_evidence = models.CharField(max_length=255, blank=True, null=True)
    
    # 6.01 Approval
    selection_evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="supplier_selections_evaluated", verbose_name="Selection Evaluator"
    )

    # --- QCL-FRM-6.03 Fields ---"""

content = content.replace(old_supp, new_supp)
with open(path, 'w') as f: f.write(content)
print("Added 6.01 fields to Supplier model.")
