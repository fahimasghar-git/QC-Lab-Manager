import re

path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'
with open(path, 'r') as f:
    content = f.read()

new_rule = """
## 📐 Core Architectural Principles
1. **1:1 Data Entry Rule:** Every field or signature line visible on a physical ISO printout MUST have a corresponding data entry field in the Django Admin backend.
2. **Digital Chain of Approval:** All forms requiring signatures (Prepared By, Checked By, Approved By) will eventually utilize a digital approval workflow (Admin Actions) where the logged-in user clicks 'Approve', capturing their timestamp and name, similar to the Sample/CoA verification workflow.

## 📊 Forms Digitization Status
"""
content = content.replace('## 📊 Forms Digitization Status', new_rule)

with open(path, 'w') as f:
    f.write(content)
print("Blueprint updated with the digital signature rule.")
