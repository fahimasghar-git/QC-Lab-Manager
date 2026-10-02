path = 'lims_core/admin_mixins.py'
with open(path, 'r') as f:
    content = f.read()

# Replace all simple hasattr checks with one that also handles signature_status
import re
content = re.sub(r'if hasattr\(obj, .status.\):\s+obj\.status = (.+)', 
                 r"if hasattr(obj, 'status'): obj.status = \1\n                elif hasattr(obj, 'signature_status'): obj.signature_status = \1", 
                 content)

with open(path, 'w') as f:
    f.write(content)
