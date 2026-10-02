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
    
    # Let's find the img tag by finding '<img src="data:image/jpeg;base64,' and its closing '/>'
    start_idx = content.find('<img src="data:image/jpeg;base64,')
    if start_idx != -1:
        end_idx = content.find('/>', start_idx) + 2
        
        # Now find the enclosing <td>
        td_start = content.rfind('<td', 0, start_idx)
        td_end = content.find('</td>', end_idx) + 5
        
        # Check if this td contains "PNAC Logo"
        td_content = content[td_start:td_end]
        if 'PNAC' in td_content:
            print(f"Removing PNAC <td> from {fpath}")
            new_content = content[:td_start] + content[td_end:]
            
            # Adjust width
            if 'width: 45%;' in new_content:
                new_content = new_content.replace('width: 45%;', 'width: 60%;', 1)
            elif 'width: 60%;' in new_content:
                new_content = new_content.replace('width: 60%;', 'width: 75%;', 1)
                
            with open(full_path, 'w') as f:
                f.write(new_content)
        else:
            print(f"Found base64 but no PNAC text in {fpath}")

