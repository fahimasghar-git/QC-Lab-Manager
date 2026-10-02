import base64
import os

# 1. Read the REAL images from the docx extraction
logo1_path = '/tmp/docx_extract/word/media/image1.jpeg'
logo2_path = '/tmp/docx_extract/word/media/image2.png'

with open(logo1_path, 'rb') as f:
    # it's a jpeg
    logo1_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf-8')

with open(logo2_path, 'rb') as f:
    # it's a png
    logo2_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

# 2. Patch CoA
coa_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/certificate_of_analysis.html'
with open(coa_path, 'r') as f:
    coa_content = f.read()

# Since we don't know the exact base64 strings currently in the file, we can use regex to replace all data:image/png;base64,... strings.
import re
# The first img tag was for logo1, the second for logo2 in my previous script.
# Wait, let's just replace the src attributes completely.
coa_content = re.sub(r'src="data:image/[^"]+" alt="PNAC Logo"', f'src="{logo2_b64}" alt="PNAC Logo"', coa_content)
coa_content = re.sub(r'src="data:image/[^"]+" alt="VAN Logo"', f'src="{logo1_b64}" alt="VAN Logo"', coa_content)

# If alt tags were not present in CoA (they weren't, I only added them to AR in the previous script!), let's replace by position.
# Let's just find all img tags and replace them.
imgs = re.findall(r'<img src="data:image/[^"]+"', coa_content)
if len(imgs) >= 2:
    coa_content = coa_content.replace(imgs[0], f'<img src="{logo2_b64}"')
    coa_content = coa_content.replace(imgs[1], f'<img src="{logo1_b64}"')

with open(coa_path, 'w') as f:
    f.write(coa_content)


# 3. Patch AR
ar_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/analysis_request.html'
with open(ar_path, 'r') as f:
    ar_content = f.read()

imgs_ar = re.findall(r'<img src="data:image/[^"]+"', ar_content)
if len(imgs_ar) >= 2:
    # Assuming the first is PNAC (image2) and second is VAN (image1)
    ar_content = ar_content.replace(imgs_ar[0], f'<img src="{logo2_b64}"')
    ar_content = ar_content.replace(imgs_ar[1], f'<img src="{logo1_b64}"')

with open(ar_path, 'w') as f:
    f.write(ar_content)

print("Real logos injected.")
