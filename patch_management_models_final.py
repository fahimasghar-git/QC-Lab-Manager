path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/models.py'
with open(path, 'r') as f:
    content = f.read()

new_models = """

# QCL-FRM-17.14 Lab Cleaning Inspection Sheet
class LabCleaningInspection(models.Model):
    history = HistoricalRecords()
    section_area = models.CharField(max_length=150, help_text="e.g. Sample Prep Room")
    month_year = models.CharField(max_length=50, help_text="e.g. October 2026")
    
    # Weekly/Monthly Tasks
    lights_acs_cleaned = models.BooleanField(default=False, verbose_name="Cleaning Of Lights and AC's (Monthly)")
    overall_spray = models.BooleanField(default=False, verbose_name="Overall Cleaning and Spray in Lab (Monthly)")
    racks_cabinets = models.BooleanField(default=False, verbose_name="Cleaning of Racks, Cabinets and Fumehood (Weekly)")
    
    def __str__(self):
        return f"{self.section_area} - {self.month_year}"

class LabCleaningDailyRecord(models.Model):
    inspection = models.ForeignKey(LabCleaningInspection, on_delete=models.CASCADE, related_name='daily_records')
    date = models.DateField()
    floor_sinks_taps = models.BooleanField(default=False, verbose_name="Floor, Sanitary Sinks and Taps")
    bench_top_shelves = models.BooleanField(default=False, verbose_name="Bench Top/Shelves")
    equipment = models.BooleanField(default=False, verbose_name="Equipment")
    checked_by = models.CharField(max_length=50, blank=True, null=True)
    verified_by = models.CharField(max_length=50, blank=True, null=True)

# QCL-FRM-20.01 Master List of Records
class MasterListRecord(models.Model):
    history = HistoricalRecords()
    title = models.CharField(max_length=200, verbose_name="Record Title")
    code = models.CharField(max_length=100, verbose_name="Record Code")
    revision_no = models.CharField(max_length=50, verbose_name="Revision No.")
    file_code = models.CharField(max_length=100, verbose_name="File code")
    location = models.CharField(max_length=200, verbose_name="File Location")
    retention_period = models.CharField(max_length=100, verbose_name="Retention Period")
    remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title

# QCL-FRM-20.02 Master List of Files and Folders
class MasterListFileFolder(models.Model):
    history = HistoricalRecords()
    file_code = models.CharField(max_length=100, verbose_name="File code")
    title = models.CharField(max_length=200, verbose_name="Title of File/Folder/Register")
    volume = models.CharField(max_length=50, verbose_name="Volume")
    keeper = models.CharField(max_length=100, verbose_name="Keeper")
    location = models.CharField(max_length=200, verbose_name="Location")
    status = models.CharField(max_length=50, verbose_name="Status")
    
    def __str__(self):
        return self.title

# QCL-FRM-21.01 Customer Feedback Form
class CustomerFeedback(models.Model):
    history = HistoricalRecords()
    customer_name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    
    SCORE_CHOICES = [(4, 'Excellent A+ (4)'), (3, 'V. Good A (3)'), (2, 'Good B (2)'), (1, 'Poor C (1)')]
    
    q1_delivery_time = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="1. How do you estimate time of delivery of our laboratory reports?")
    q2_politeness = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="2. How do you estimate politeness of our laboratory staff?")
    q3_accuracy = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="3. How do you estimate accuracy of contents of our Laboratory reports?")
    q4_response = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="4. How do you rate our response to your complaints & feedbacks?")
    q5_satisfaction = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="5. Rating of your overall satisfaction level?")
    q6_knowledge = models.IntegerField(choices=SCORE_CHOICES, default=4, verbose_name="6. How do you estimate knowledge of our laboratory analyst?")
    
    comments = models.TextField(blank=True, null=True, verbose_name="Any specific comments / complaint / suggestion or feedback you would like to add:")
    
    @property
    def total_score(self):
        return self.q1_delivery_time + self.q2_politeness + self.q3_accuracy + self.q4_response + self.q5_satisfaction + self.q6_knowledge
        
    @property
    def percentage(self):
        return round((self.total_score / 24.0) * 100, 2)
        
    def __str__(self):
        return f"Feedback - {self.customer_name} ({self.date})"
"""

content = content + "\n" + new_models

with open(path, 'w') as f:
    f.write(content)
print("Updated management/models.py")
