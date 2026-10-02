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
    
    # Regex to find the <td> containing the PNAC Logo comment and the base64 img
    # It starts with <td...>, contains <!-- PNAC Logo (Left) --> and <img src="data:image...
    # and ends with </td>
    
    pattern = r'<td[^>]*>\s*<!-- PNAC Logo \(Left\) -->\s*<img src="data:image/jpeg;base64,.*?" width="60" height="60" />\s*</td>'
    
    # Check if we can find it
    matches = re.findall(pattern, content, flags=re.DOTALL)
    if matches:
        print(f"Found in {fpath}, removing...")
        new_content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Now we need to adjust the width of the remaining columns so they add up to 100%
        # The remaining columns are: 
        # company logo (15%), title (45% -> 60%), right panel (25%). Or similar.
        # Let's just boost the title's width by 15%.
        # For analysis_request.html: <td rowspan="2" style="width: 45%; border: 1px solid #000; font-size: 16px; font-weight: bold; padding: 5px;">
        # We'll just replace 'width: 45%' with 'width: 60%' and 'width: 60%' with 'width: 75%'.
        
        # Let's see what widths are used for the title.
        title_patterns = [
            (r'width: 45%;', 'width: 60%;'),
            (r'width: 60%;', 'width: 75%;')
        ]
        for old_w, new_w in title_patterns:
            new_content = new_content.replace(old_w, new_w, 1) # replace only the first occurrence (which should be the title)
            
        with open(full_path, 'w') as f:
            f.write(new_content)
    else:
        print(f"NOT FOUND in {fpath}")

