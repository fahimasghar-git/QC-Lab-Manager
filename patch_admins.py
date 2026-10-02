import os

# --- PATCH MANAGEMENT ADMIN ---
mgt_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/admin.py'
with open(mgt_path, 'r') as f:
    mgt_content = f.read()

mgt_old = """    list_display = ('nc_id', 'identified_by', 'date_identified', 'status')
    list_filter = ('status', 'date_identified')
    search_fields = ('nc_id', 'description', 'root_cause_analysis', 'corrective_action')"""

mgt_new = """    list_display = ('nc_id', 'source', 'nc_type', 'level_of_risk', 'status')
    list_filter = ('status', 'source', 'nc_type', 'level_of_risk')
    search_fields = ('nc_id', 'description', 'root_cause_analysis', 'corrective_action')
    
    fieldsets = (
        ('QCL-FRM-14.01 (Non-Conformance Details)', {
            'fields': ('nc_id', 'source', 'nc_type', 'level_of_risk', 'impact_on_previous_result', 'date_identified', 'identified_by')
        }),
        ('Investigation & Description', {
            'fields': ('description', 'related_test')
        }),
        ('Root Cause & CAPA (QCL-FRM-14.03)', {
            'fields': ('root_cause_analysis', 'corrective_action', 'status')
        }),
        ('Decisions & Actions', {
            'fields': ('acceptance_status', 'withhold_reports', 'halt_work', 'recall_work')
        }),
        ('Signatures', {
            'fields': ('evaluated_by', 'reviewed_by')
        }),
    )"""

mgt_content = mgt_content.replace(mgt_old, mgt_new)
with open(mgt_path, 'w') as f:
    f.write(mgt_content)


# --- PATCH RESOURCES ADMIN ---
res_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(res_path, 'r') as f:
    res_content = f.read()

res_old = """    list_display = ('name', 'contact_person', 'email', 'phone', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('name', 'contact_person')"""

res_new = """    list_display = ('name', 'evaluation_type', 'decision', 'is_approved')
    list_filter = ('is_approved', 'evaluation_type', 'decision')
    search_fields = ('name', 'contact_person')
    
    fieldsets = (
        ('Supplier Details', {
            'fields': ('name', 'contact_person', 'email', 'phone')
        }),
        ('QCL-FRM-6.03 (Evaluation Profile)', {
            'fields': ('evaluation_type', 'sample_approved_by_qc', 'decision', 'remarks')
        }),
        ('QCL-FRM-6.03 (Scoring)', {
            'fields': ('score_market_image', 'score_market_share', 'score_technical_capacity', 'score_lead_time', 'score_product_quality', 'score_order_processing', 'score_fulfill_requirements')
        }),
        ('ISO 17025 Status', {
            'fields': ('is_approved', 'last_evaluation_date', 'next_evaluation_date', 'evaluation_notes')
        }),
    )"""

res_content = res_content.replace(res_old, res_new)
with open(res_path, 'w') as f:
    f.write(res_content)

