path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'

with open(path, 'r') as f:
    content = f.read()

old_next = """## 🛠️ Next Steps

1. **Finish Clause 6.6:** Digitize the final two purchasing forms (QCL-FRM-6.05 Comparative Statement, QCL-FRM-6.06 Supplier Evaluation Plan).
2. **Audits & Non-Conformance:** Expand the existing NC models to generate the 14.02 Log and 14.03 Root Cause Analysis standalone forms.
3. **Personnel & Authorization:** Build out the Personnel Authorization (1.01, 1.02) tracking."""

new_next = """## 🛠️ Next Steps

1. **Audits & Non-Conformance:** Expand the existing NC models to generate the 14.02 Log and 14.03 Root Cause Analysis standalone forms.
2. **Process & QA:** Knock out the forms in Clause 7 & 8 (Lab Cleaning 17.14, Master Lists 20.01/20.02, Feedback 21.01)."""

content = content.replace(old_next, new_next)

with open(path, 'w') as f:
    f.write(content)
