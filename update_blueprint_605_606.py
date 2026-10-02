path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'

with open(path, 'r') as f:
    content = f.read()

# Update stats
content = content.replace("Fully Digitized:** 17 (62%)", "Fully Digitized:** 19 (70%)")
content = content.replace("Pending:** 10 (37%)", "Pending:** 8 (30%)")

# Remove from pending
pending_clause = "**Clause 6.6 (External Providers & Purchasing)**\n- [ ] **QCL-FRM-6.05** - Comparative Statement\n- [ ] **QCL-FRM-6.06** - Supplier Evaluation Plan\n\n"
content = content.replace(pending_clause, "")

# Add to completed under Clause 6.6
insert_target = "**Clause 6.6 (External Providers & Purchasing)**\n"
new_completed = insert_target + "- [x] **QCL-FRM-6.05** - Comparative Statement\n- [x] **QCL-FRM-6.06** - Supplier Evaluation Plan\n"
content = content.replace(insert_target, new_completed)

with open(path, 'w') as f:
    f.write(content)

print("Blueprint updated with 6.05 and 6.06.")
