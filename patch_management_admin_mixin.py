import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/admin.py'
with open(path, 'r') as f:
    content = f.read()

# Add import
import_statement = "from lims_core.admin_mixins import DigitalSignatureMixin\n"
content = import_statement + content

# Replace MasterListRecordAdmin
content = content.replace(
    "class MasterListRecordAdmin(ModelAdmin, SimpleHistoryAdmin):",
    "class MasterListRecordAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):"
)

# Replace MasterListFileFolderAdmin
content = content.replace(
    "class MasterListFileFolderAdmin(ModelAdmin, SimpleHistoryAdmin):",
    "class MasterListFileFolderAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):"
)

with open(path, 'w') as f:
    f.write(content)
