import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/lims_core/settings.py'
with open(path, 'r') as f:
    content = f.read()

# Make sure STATICFILES_DIRS is there
if 'STATICFILES_DIRS =' not in content:
    content = content.replace("STATIC_URL = 'static/'", "STATIC_URL = 'static/'\nSTATICFILES_DIRS = [BASE_DIR / 'static_assets']\n")
    with open(path, 'w') as f:
        f.write(content)
