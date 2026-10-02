import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/admin.py'
with open(path, 'r') as f:
    content = f.read()

content = "from lims_core.admin_mixins import DigitalSignatureMixin\n" + content
content = content.replace("class SampleReturnAdmin(ModelAdmin, SimpleHistoryAdmin):", "class SampleReturnAdmin(DigitalSignatureMixin, ModelAdmin, SimpleHistoryAdmin):")
with open(path, 'w') as f:
    f.write(content)
