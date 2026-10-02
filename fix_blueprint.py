path = '/Users/fahimasghar/.gemini/antigravity/brain/92c2e6e3-0cd4-4132-971d-a7f129b6d815/iso17025_lims_blueprint.md'

with open(path, 'r') as f:
    content = f.read()

bad_string = """---


- [ ] **QCL-FRM-22.01** - Sample Return Form

---"""

content = content.replace(bad_string, "")

with open(path, 'w') as f:
    f.write(content)
