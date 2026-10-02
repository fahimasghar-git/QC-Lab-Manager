path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'

with open(path, 'r') as f:
    content = f.read()

# Update stats
content = content.replace("Fully Digitized:** 19 (70%)", "Fully Digitized:** 21 (77%)")
content = content.replace("Pending:** 8 (30%)", "Pending:** 6 (22%)")

# Remove from pending
pending_clause = "**Clause 8.7 (Non-Conformances & Corrective Actions)**\n- [ ] **QCL-FRM-14.02** - Non-Conformance Log *(Can be derived from existing NC DB)*\n- [ ] **QCL-FRM-14.03** - Root Cause Analysis Form\n\n"
content = content.replace(pending_clause, "")

# Add to completed under Clause 8
insert_target = "**Clause 8 (Management System - Non-Conformance)**\n"
new_completed = insert_target + "- [x] **QCL-FRM-14.01** - Non-Conformance Form\n- [x] **QCL-FRM-14.02** - Non-Conformance Log\n- [x] **QCL-FRM-14.03** - Root Cause Analysis Form\n"
content = content.replace(insert_target + "- [x] **QCL-FRM-14.01** - Non-Conformance Form\n", new_completed)

with open(path, 'w') as f:
    f.write(content)

print("Blueprint updated with 14.02 and 14.03.")
