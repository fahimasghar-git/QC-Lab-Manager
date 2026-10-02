path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'

with open(path, 'r') as f:
    content = f.read()

# Update stats
content = content.replace("Fully Digitized:** 21 (77%)", "Fully Digitized:** 27 (100%)")
content = content.replace("Pending:** 6 (22%)", "Pending:** 0 (0%)")

# Remove all pending forms text
pending_section = """### 📝 Pending Digitization
*These forms are currently sitting in the ISO 17025 folder and have not yet been mapped into the LIMS.*

**Clause 7 & 8 (Process & Quality Assurance)**
- [ ] **QCL-FRM-17.14** - Lab Cleaning Inspection Sheet
- [ ] **QCL-FRM-19.01** - Assignment, Summary and Review Form
- [ ] **QCL-FRM-20.01** - Master List of Records
- [ ] **QCL-FRM-20.02** - Master List of Files and Folders
- [ ] **QCL-FRM-21.01** - Customer Feedback Form"""
content = content.replace(pending_section, "")

# Find places to put the newly completed forms
# 19.01 goes to Clause 7
c7 = "**Clause 7 (Process Requirements - Samples)**\n- [x] **QCL-FRM-12.01** - Analysis Request\n- [x] **QCL-FRM-12.03** - Certificate of Analysis"
new_c7 = "**Clause 7 (Process Requirements - Samples)**\n- [x] **QCL-FRM-12.01** - Analysis Request\n- [x] **QCL-FRM-12.03** - Certificate of Analysis\n- [x] **QCL-FRM-19.01** - Assignment, Summary and Review Form\n- [x] **QCL-FRM-22.01** - Sample Return Form"
content = content.replace(c7, new_c7)

# 17.14, 20.01, 20.02, 21.01 go to Clause 8 (or create new clause block)
c8 = "**Clause 8 (Management System - Non-Conformance)**\n- [x] **QCL-FRM-14.01** - Non-Conformance Form\n- [x] **QCL-FRM-14.02** - Non-Conformance Log\n- [x] **QCL-FRM-14.03** - Root Cause Analysis Form\n"
new_c8 = """**Clause 8 (Management System - Non-Conformance & QA)**
- [x] **QCL-FRM-14.01** - Non-Conformance Form
- [x] **QCL-FRM-14.02** - Non-Conformance Log
- [x] **QCL-FRM-14.03** - Root Cause Analysis Form
- [x] **QCL-FRM-17.14** - Lab Cleaning Inspection Sheet
- [x] **QCL-FRM-20.01** - Master List of Records
- [x] **QCL-FRM-20.02** - Master List of Files and Folders
- [x] **QCL-FRM-21.01** - Customer Feedback Form\n"""
content = content.replace(c8, new_c8)

# Update Next Steps
old_next = """## 🛠️ Next Steps

1. **Process & QA:** Knock out the remaining general forms in Clause 7 & 8 (Lab Cleaning 17.14, Master Lists 20.01/20.02, Feedback 21.01, Sample Return 22.01).
2. **Final Review:** Perform UAT with QC team once all forms are digitialized."""
new_next = """## 🛠️ Next Steps

1. **User Acceptance Testing (UAT):** Review the 27 digitized forms with the QC Team.
2. **Digital Signatures:** Expand permissions matrix to handle Submit -> Verify -> Approve electronically.
3. **Cloud Deployment:** Migrate from SQLite to PostgreSQL and host on AWS/DigitalOcean."""
content = content.replace(old_next, new_next)

with open(path, 'w') as f:
    f.write(content)
print("Blueprint updated to 100%.")
