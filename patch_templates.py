import re

# 1. Competency Report
p1 = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/competency_report.html'
with open(p1, 'r') as f: c1 = f.read()
c1 = c1.replace('_________________________<br><strong>Prepared By</strong>', '{{ record.prepared_by.get_full_name|default:"_________________________" }}<br><strong>Prepared By</strong>')
c1 = c1.replace('_________________________<br><strong>Checked By</strong>', '{{ record.checked_by.get_full_name|default:"_________________________" }}<br><strong>Checked By</strong>')
c1 = c1.replace('_________________________<br><strong>Approved By</strong>', '{{ record.approved_by.get_full_name|default:"_________________________" }}<br><strong>Approved By</strong>')
with open(p1, 'w') as f: f.write(c1)

# 2. Competency Evaluation
p2 = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/competency_evaluation_report.html'
with open(p2, 'r') as f: c2 = f.read()
c2 = c2.replace('_________________________<br><strong>Manager QC</strong>', '{{ eval.manager_qc.get_full_name|default:"_________________________" }}<br><strong>Manager QC</strong>')
with open(p2, 'w') as f: f.write(c2)

# 3. Store Purchase Demand
p3 = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/store_purchase_demand.html'
with open(p3, 'r') as f: c3 = f.read()
# We are iterating over `requests` which is a QuerySet. For header fields, we can just use `requests.0`.
c3 = c3.replace('<strong>SPD No:</strong> _______________________', '<strong>SPD No:</strong> {{ requests.0.spd_no|default:"_______________________" }}')
c3 = c3.replace('<strong>Date:</strong> _______________________', '<strong>Date:</strong> {{ requests.0.requested_date|date:"d-M-Y"|default:"_______________________" }}')
c3 = c3.replace('<strong>Insp Mints NO & Date:</strong> _______________________', '<strong>Insp Mints NO & Date:</strong> {{ requests.0.insp_mints_no|default:"_______________________" }}')
c3 = c3.replace('<strong>Service Call No & Date:</strong> _______________________', '<strong>Service Call No & Date:</strong> {{ requests.0.service_call_no|default:"_______________________" }}')
c3 = c3.replace('<td>_________________________<br><strong>Indentor</strong></td>', '<td>{{ requests.0.requested_by.get_full_name|default:"_________________________" }}<br><strong>Indentor</strong></td>')
c3 = c3.replace('<td>_________________________<br><strong>Store Keeper</strong></td>', '<td>{{ requests.0.store_keeper.get_full_name|default:"_________________________" }}<br><strong>Store Keeper</strong></td>')
c3 = c3.replace('<td>_________________________<br><strong>Plant Manager</strong></td>', '<td>{{ requests.0.approved_by.get_full_name|default:"_________________________" }}<br><strong>Plant Manager</strong></td>')
with open(p3, 'w') as f: f.write(c3)

# 4. Equipment Master List
p4 = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/equipment_master_list.html'
with open(p4, 'r') as f: c4 = f.read()
c4 = c4.replace('<td>_________________________<br><strong>Prepared By (AQCM)</strong><br><br>Date:</td>', '<td>{{ equipments.0.prepared_by.get_full_name|default:"_________________________" }}<br><strong>Prepared By (AQCM)</strong><br><br>Date:</td>')
c4 = c4.replace('<td>_________________________<br><strong>Reviewed By (QCM)</strong><br><br>Date:</td>', '<td>{{ equipments.0.reviewed_by.get_full_name|default:"_________________________" }}<br><strong>Reviewed By (QCM)</strong><br><br>Date:</td>')
c4 = c4.replace('<td>_________________________<br><strong>Approved By (CEO)</strong><br><br>Date:</td>', '<td>{{ equipments.0.approved_by.get_full_name|default:"_________________________" }}<br><strong>Approved By (CEO)</strong><br><br>Date:</td>')
with open(p4, 'w') as f: f.write(c4)

# 5. Equipment Maintenance
p5 = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/equipment_maintenance_record.html'
with open(p5, 'r') as f: c5 = f.read()
c5 = c5.replace('<td>_________________________<br><strong>Prepared By (AQCM)</strong><br><br>Date:</td>', '<td>{{ maintenances.0.prepared_by.get_full_name|default:"_________________________" }}<br><strong>Prepared By (AQCM)</strong><br><br>Date:</td>')
c5 = c5.replace('<td>_________________________<br><strong>Reviewed By (QCM)</strong><br><br>Date:</td>', '<td>{{ maintenances.0.reviewed_by.get_full_name|default:"_________________________" }}<br><strong>Reviewed By (QCM)</strong><br><br>Date:</td>')
c5 = c5.replace('<td>_________________________<br><strong>Approved By (CEO)</strong><br><br>Date:</td>', '<td>{{ maintenances.0.approved_by.get_full_name|default:"_________________________" }}<br><strong>Approved By (CEO)</strong><br><br>Date:</td>')
with open(p5, 'w') as f: f.write(c5)

# 6. Calibration Program
p6 = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/calibration_program.html'
with open(p6, 'r') as f: c6 = f.read()
c6 = c6.replace('<td>_________________________<br><strong>Prepared By (AQCM)</strong><br><br>Date:</td>', '<td>{{ equipments.0.prepared_by.get_full_name|default:"_________________________" }}<br><strong>Prepared By (AQCM)</strong><br><br>Date:</td>')
c6 = c6.replace('<td>_________________________<br><strong>Reviewed By (QCM)</strong><br><br>Date:</td>', '<td>{{ equipments.0.reviewed_by.get_full_name|default:"_________________________" }}<br><strong>Reviewed By (QCM)</strong><br><br>Date:</td>')
c6 = c6.replace('<td>_________________________<br><strong>Approved By (CEO)</strong><br><br>Date:</td>', '<td>{{ equipments.0.approved_by.get_full_name|default:"_________________________" }}<br><strong>Approved By (CEO)</strong><br><br>Date:</td>')
with open(p6, 'w') as f: f.write(c6)

print("All templates patched.")
