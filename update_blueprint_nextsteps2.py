path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'

with open(path, 'r') as f:
    content = f.read()

old_next = """## 🛠️ Next Steps

1. **Audits & Non-Conformance:** Expand the existing NC models to generate the 14.02 Log and 14.03 Root Cause Analysis standalone forms.
2. **Process & QA:** Knock out the forms in Clause 7 & 8 (Lab Cleaning 17.14, Master Lists 20.01/20.02, Feedback 21.01)."""

new_next = """## 🛠️ Next Steps

1. **Process & QA:** Knock out the remaining general forms in Clause 7 & 8 (Lab Cleaning 17.14, Master Lists 20.01/20.02, Feedback 21.01, Sample Return 22.01).
2. **Final Review:** Perform UAT with QC team once all forms are digitialized."""

content = content.replace(old_next, new_next)

with open(path, 'w') as f:
    f.write(content)
