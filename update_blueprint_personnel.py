path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'

with open(path, 'r') as f:
    content = f.read()

# Update stats
content = content.replace("Fully Digitized:** 15 (55%)", "Fully Digitized:** 17 (62%)")
content = content.replace("Pending:** 12 (45%)", "Pending:** 10 (37%)")

# Remove from pending
content = content.replace("**Clause 6.2 (Personnel Authorizations)**\n- [ ] **QCL-FRM-1.01** - Personnel Authorization Permit\n- [ ] **QCL-FRM-1.02** - List of Authorized Staff\n\n", "")

# Add to completed under Clause 5 & 6
insert_target = "**Clause 5 & 6 (Structural & Resource Requirements)**\n"
new_completed = insert_target + "- [x] **QCL-FRM-1.01** - Personnel Authorization Permit\n- [x] **QCL-FRM-1.02** - List of Authorized Staff\n"
content = content.replace(insert_target, new_completed)

with open(path, 'w') as f:
    f.write(content)

print("Blueprint updated with 1.01 and 1.02.")
