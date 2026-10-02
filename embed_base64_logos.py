import base64
import os

# 1. Read images and convert to base64
logo1_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/static/images/logo1.png'
logo2_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/static/images/logo2.png'

with open(logo1_path, 'rb') as f:
    logo1_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

with open(logo2_path, 'rb') as f:
    logo2_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

# 2. Patch CoA
coa_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/certificate_of_analysis.html'
with open(coa_path, 'r') as f:
    coa_content = f.read()

# Replace src in CoA
coa_content = coa_content.replace('src="/Users/fahimasghar/Documents/QC-Lab-Manager/static/images/logo1.png"', f'src="{logo1_b64}"')
coa_content = coa_content.replace('src="/Users/fahimasghar/Documents/QC-Lab-Manager/static/images/logo2.png"', f'src="{logo2_b64}"')

with open(coa_path, 'w') as f:
    f.write(coa_content)

# 3. Patch AR
ar_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/analysis_request.html'
with open(ar_path, 'r') as f:
    ar_content = f.read()

# Replace src in AR
ar_content = ar_content.replace('src="{% static \'images/logo1.png\' %}"', f'src="{logo1_b64}"')
ar_content = ar_content.replace('src="{% static \'images/logo2.png\' %}"', f'src="{logo2_b64}"')

with open(ar_path, 'w') as f:
    f.write(ar_content)

print("Base64 injection complete.")
