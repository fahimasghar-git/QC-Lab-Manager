file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/testing/admin.py'
with open(file_path, 'r') as f:
    content = f.read()

old_list = "list_display = ('id', 'sample', 'result_type', 'parameter', 'result_value', 'unit', 'get_qc_metrics', 'status', 'analyst')"
new_list = "list_display = ('id', 'sample', 'result_type', 'parameter', 'assigned_to', 'result_value', 'unit', 'status', 'analyst')\n    list_editable = ('assigned_to', 'status')\n    actions = [submit_test_for_verification, verify_test_result]"
content = content.replace(old_list, new_list)

with open(file_path, 'w') as f:
    f.write(content)
