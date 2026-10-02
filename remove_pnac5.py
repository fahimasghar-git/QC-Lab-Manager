import os

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
    
    # Let's find all occurrences of '<td' and '</td>'
    start = 0
    new_content = content
    found = False
    
    while True:
        td_start = new_content.find('<td', start)
        if td_start == -1:
            break
        td_end = new_content.find('</td>', td_start) + 5
        
        td_html = new_content[td_start:td_end]
        
        # Check if it has PNAC inside (either in comment or alt attribute)
        if 'PNAC' in td_html and 'data:image/jpeg;base64' in td_html:
            print(f"Removing PNAC <td> from {fpath}")
            new_content = new_content[:td_start] + new_content[td_end:]
            found = True
            break
        else:
            start = td_start + 1
            
    if found:
        # Adjust width
        if 'width: 45%;' in new_content:
            new_content = new_content.replace('width: 45%;', 'width: 60%;', 1)
        elif 'width: 60%;' in new_content:
            new_content = new_content.replace('width: 60%;', 'width: 75%;', 1)
            
        with open(full_path, 'w') as f:
            f.write(new_content)

