path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'
with open(path, 'r') as f:
    content = f.read()

# Replace pending list entries for 6.03, 14.01, 5.01
updates = [
    ("- [ ] **QCL-FRM-6.03** - Supplier Evaluation Form", "- [x] **QCL-FRM-6.03** - Supplier Evaluation Form"),
    ("- [ ] **QCL-FRM-14.01** - Non-Conformance / Corrective Actions", "- [x] **QCL-FRM-14.01** - Non-Conformance / Corrective Actions"),
    ("- [ ] **QCL-FRM-5.01** - CRM List (Metrological Traceability / ReagentStandards)", "- [x] **QCL-FRM-5.01** - CRM List (Metrological Traceability / ReagentStandards)")
]

for old, new in updates:
    content = content.replace(old, new)

with open(path, 'w') as f:
    f.write(content)
