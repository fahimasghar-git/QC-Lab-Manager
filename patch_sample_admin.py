import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/admin.py'
with open(path, 'r') as f: content = f.read()

old_fs = """    fieldsets = (
        ('Sample Identification', {
            'fields': ('sample_id', 'client', 'product_name', 'batch_number')
        }),
        ('Condition & Storage', {
            'fields': ('description', 'storage_condition', 'status')
        }),
        ('Chain of Custody', {
            'fields': ('received_by', 'received_date', 'notes')
        }),
        ('ISO 17025 Authorization', {
            'fields': ('verified_by', 'verified_at', 'approved_by', 'approved_at')
        }),
    )"""
new_fs = """    fieldsets = (
        ('Sample Identification & AR Details', {
            'fields': ('sample_id', 'serial_number', 'client', 'product_name', 'batch_number', 'sample_quantity', 'assay')
        }),
        ('Condition & Storage', {
            'fields': ('description', 'storage_condition', 'status', 'rejection_reason')
        }),
        ('Chain of Custody & Signatures', {
            'fields': ('customer_signature', 'received_by', 'received_date', 'notes')
        }),
        ('ISO 17025 Authorization', {
            'fields': ('verified_by', 'verified_at', 'approved_by', 'approved_at')
        }),
    )"""
content = content.replace(old_fs, new_fs)
with open(path, 'w') as f: f.write(content)
print("Updated SampleAdmin fieldsets.")
