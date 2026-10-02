import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
with open(path, 'r') as f:
    content = f.read()

new_model = """
class PersonnelAuthorization(models.Model):
    history = HistoricalRecords()

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authorization_permit')
    employee_code = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    
    # 1.01 Instrument Operation
    op_flame_photometer = models.BooleanField(default=False, verbose_name="Operation of Flame Photometer")
    op_uv_vis = models.BooleanField(default=False, verbose_name="Operation of UV-Visible Spectrophotometer")
    op_karl_fischer = models.BooleanField(default=False, verbose_name="Operation of Karl Fischer")
    op_kjeldhals = models.BooleanField(default=False, verbose_name="Operation of Kjeldhal’s Apparatus")
    op_furnace = models.BooleanField(default=False, verbose_name="Operation of Furnace")
    op_ph_meter = models.BooleanField(default=False, verbose_name="Operation of pH Meter")
    op_tds_meter = models.BooleanField(default=False, verbose_name="Operation of TDS Meter")
    op_analytical_balance = models.BooleanField(default=False, verbose_name="Operation of Analytical Balance")
    
    # 1.01 Tests & Parameters
    test_loi = models.BooleanField(default=False, verbose_name="Loss on Ignition")
    test_density = models.BooleanField(default=False, verbose_name="Density Test")
    test_ph = models.BooleanField(default=False, verbose_name="pH Test")
    test_conductivity = models.BooleanField(default=False, verbose_name="Conductivity Test")
    test_tds = models.BooleanField(default=False, verbose_name="TDS Test")
    test_lod = models.BooleanField(default=False, verbose_name="Loss on Drying")
    test_weighing = models.BooleanField(default=False, verbose_name="Weighing")
    test_sieve = models.BooleanField(default=False, verbose_name="Sieve Test")
    test_calcium = models.BooleanField(default=False, verbose_name="Calcium test")
    test_sulfur = models.BooleanField(default=False, verbose_name="Sulfur/Sulfate Test")
    test_nitrogen = models.BooleanField(default=False, verbose_name="Nitrogen Test")
    test_titrations = models.BooleanField(default=False, verbose_name="Manual Titrations")
    test_humic_acid = models.BooleanField(default=False, verbose_name="Humic Acid Test")
    test_phosphorus = models.BooleanField(default=False, verbose_name="Phosphorus Testing")
    test_toc = models.BooleanField(default=False, verbose_name="Total Organic Carbon")
    test_cn_ratio = models.BooleanField(default=False, verbose_name="C/N Ratio Calculation")
    test_organic_matter = models.BooleanField(default=False, verbose_name="Organic Matter")
    test_cec = models.BooleanField(default=False, verbose_name="CEC")
    test_sodium = models.BooleanField(default=False, verbose_name="Sodium Test")
    test_zinc = models.BooleanField(default=False, verbose_name="Zinc Test")
    test_boron = models.BooleanField(default=False, verbose_name="Boron Analysis")
    test_copper = models.BooleanField(default=False, verbose_name="Copper Test")
    test_moisture = models.BooleanField(default=False, verbose_name="Moisture Test")
    
    # 1.01 Quality & Lab Activities
    act_environmental = models.BooleanField(default=False, verbose_name="Monitoring Environmental Conditions")
    act_intermediate_checks = models.BooleanField(default=False, verbose_name="Perform the Intermediate Checks")
    act_control_chart = models.BooleanField(default=False, verbose_name="Prepare Control Chart")
    act_sample_receiving = models.BooleanField(default=False, verbose_name="Sample Receiving")
    act_method_validation = models.BooleanField(default=False, verbose_name="Method Validation/Verification")
    act_sample_handling = models.BooleanField(default=False, verbose_name="Sample Handling")
    act_report_prep = models.BooleanField(default=False, verbose_name="Report Preparation")
    act_review_reports = models.BooleanField(default=False, verbose_name="Preparing/Review the Analysis Reports")
    act_measurement_uncertainty = models.BooleanField(default=False, verbose_name="Measurements of Uncertainty")
    act_internal_auditing = models.BooleanField(default=False, verbose_name="Internal Auditing")
    act_training_lms = models.BooleanField(default=False, verbose_name="Training of Lab Staff on LMS 17025:2017")
    act_prep_procedures = models.BooleanField(default=False, verbose_name="Preparation and Reviewing of Procedures/Other Documents")
    act_approve_reports = models.BooleanField(default=False, verbose_name="Preparation, Reviewing and Approved of Reports/Other Documents")
    act_prep_release_slip = models.BooleanField(default=False, verbose_name="Preparation and Review/Verify the Release slip")
    act_practical_demo = models.BooleanField(default=False, verbose_name="Practical Demonstration of Testing Parameters")
    act_assign_samples = models.BooleanField(default=False, verbose_name="Assigned the samples for testing to analysts/assistant analyst")
    act_analyze_samples = models.BooleanField(default=False, verbose_name="Analyzed the samples")
    act_housekeeping = models.BooleanField(default=False, verbose_name="House Keeping")
    act_solution_prep = models.BooleanField(default=False, verbose_name="Solution Preparation")
    act_sample_retaining = models.BooleanField(default=False, verbose_name="Sample Retaining")
    act_sample_discard = models.BooleanField(default=False, verbose_name="Sample Discard/Dispose")
    act_stock_management = models.BooleanField(default=False, verbose_name="Stock Management")
    act_id_non_conformity = models.BooleanField(default=False, verbose_name="Identification of Non-Conformity")
    act_id_improvement = models.BooleanField(default=False, verbose_name="Identification of Need for improvement or Deviation")
    act_temp_humidity = models.BooleanField(default=False, verbose_name="Prepare the temperature/humidity charts")
    act_cleaning_inspections = models.BooleanField(default=False, verbose_name="Perform the Cleaning Inspections")
    act_standardization = models.BooleanField(default=False, verbose_name="Standardization")
    act_pt_samples = models.BooleanField(default=False, verbose_name="PT Samples/Blind Samples")
    
    # 1.02 Master List Authorizations
    auth_dev_mod = models.BooleanField(default=False, verbose_name="Development & Modification")
    auth_perform = models.BooleanField(default=False, verbose_name="Perform")
    auth_validation = models.BooleanField(default=False, verbose_name="Validation / Verification")
    auth_supervision = models.BooleanField(default=False, verbose_name="Supervision")
    auth_report_review = models.BooleanField(default=False, verbose_name="Report and Review of Results")
    auth_analysis_results = models.BooleanField(default=False, verbose_name="Analysis of results (Conformity/Opinions)")
    auth_auth_results = models.BooleanField(default=False, verbose_name="Authorization of Results")
    auth_uncertainty = models.BooleanField(default=False, verbose_name="Uncertainty Measurement of Assay")
    
    authorization_date = models.DateField(auto_now_add=True)
    
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='prepared_authorizations', on_delete=models.RESTRICT, null=True, blank=True)
    authorized_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='authorized_authorizations', on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        verbose_name = 'Personnel Authorization (1.01 & 1.02)'
        verbose_name_plural = 'Personnel Authorizations (1.01 & 1.02)'

    def __str__(self):
        return f"Authorization Permit - {self.user.get_full_name() or self.user.username}"

"""

content = content + "\n" + new_model

with open(path, 'w') as f:
    f.write(content)
print("PersonnelAuthorization model added to resources/models.py")
