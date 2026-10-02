import os
import re

files = [
    'management/templates/management/non_conformance_form.html',
    'resources/templates/resources/store_purchase_demand.html',
    'resources/templates/resources/calibration_program.html',
    'resources/templates/resources/competency_evaluation_report.html',
    'resources/templates/resources/equipment_maintenance_record.html',
    'resources/templates/resources/equipment_master_list.html',
    'resources/templates/resources/supplier_evaluation.html',
    'resources/templates/resources/competency_report.html',
    'samples/templates/samples/analysis_request.html'
]

base_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager/'

for fpath in files:
    full_path = os.path.join(base_dir, fpath)
    with open(full_path, 'r') as f:
        content = f.read()
    
    # We will search for the <td> block containing the base64 image
    pattern = r'<td[^>]*>\s*<!-- PNAC Logo \(Left\) -->.*?</td>'
    
    matches = re.findall(pattern, content, flags=re.DOTALL)
    if matches:
        print(f"Found in {fpath}, removing...")
        # Remove the td
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Adjust width of the title TD which is typically the next TD with rowspan="3" or "2"
        # Since we removed 15% width, we need to add 15% width somewhere.
        # "width: 45%;" -> "width: 60%;"
        # "width: 60%;" -> "width: 75%;"
        content = content.replace('width: 45%;', 'width: 60%;', 1)
        content = content.replace('width: 60%;', 'width: 75%;', 1)
        
        with open(full_path, 'w') as f:
            f.write(content)
    else:
        print(f"NOT FOUND in {fpath}")

