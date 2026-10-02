import re

path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'
with open(path, 'r') as f:
    content = f.read()

# Replace pending list entries for 6.01, 6.02, 6.04, 6.08
updates = [
    ("- [ ] QCL-FRM-6.01 - Supplier Selection Form", "- [x] QCL-FRM-6.01 - Supplier Selection Form"),
    ("- [ ] QCL-FRM-6.02 - Approved Supplier / Service Provider List", "- [x] QCL-FRM-6.02 - Approved Supplier / Service Provider List"),
    ("- [ ] QCL-FRM-6.04 - Supplier Performance Monitoring", "- [x] QCL-FRM-6.04 - Supplier Performance Monitoring"),
    ("- [ ] QCL-FRM-6.08 - Products/Services Inspection Form", "- [x] QCL-FRM-6.08 - Products/Services Inspection Form")
]

for old, new in updates:
    content = content.replace(old, new)

with open(path, 'w') as f:
    f.write(content)
