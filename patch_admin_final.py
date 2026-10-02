file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/testing/admin.py'
with open(file_path, 'r') as f:
    content = f.read()

# Fix 1: Remove @admin.register(TestResult) from above the function
content = content.replace("@admin.register(TestResult)\ndef submit_test_for_verification", "@admin.action(description='▶️ Submit Result for AQCM Verification')\ndef submit_test_for_verification")

# Fix 2: Add @admin.register(TestResult) back above the class
content = content.replace("class TestResultAdmin(ModelAdmin, SimpleHistoryAdmin):", "@admin.register(TestResult)\nclass TestResultAdmin(ModelAdmin, SimpleHistoryAdmin):")

with open(file_path, 'w') as f:
    f.write(content)
