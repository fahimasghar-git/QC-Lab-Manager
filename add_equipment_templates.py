import re
import os

comp_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/competency_report.html'
with open(comp_path, 'r') as f:
    comp_content = f.read()

imgs = re.findall(r'<img src="(data:image/[^"]+)"', comp_content)
logo2_b64 = imgs[0] if len(imgs) > 0 else ""
logo1_b64 = imgs[1] if len(imgs) > 1 else ""

template_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources'

def get_base_html(title, format_no, revision_no, table_headers, loop_var, row_template, is_landscape=True):
    landscape_css = "@page { size: landscape; }" if is_landscape else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 11px; margin: 20px; }}
        {landscape_css}
        .header-table {{ width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 20px; text-align: center; }}
        .header-table td {{ border: 1px solid #000; padding: 5px; }}
        
        .main-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 11px; }}
        .main-table th, .main-table td {{ border: 1px solid #000; padding: 6px; text-align: center; vertical-align: middle; }}
        .main-table th {{ background-color: #f2f2f2; font-weight: bold; }}
        
        @media print {{
            button {{ display: none; }}
            body {{ margin: 0; }}
        }}
    </style>
</head>
<body>
    <button onclick="window.print()" style="padding: 10px 20px; margin-bottom: 20px; font-size: 14px; cursor: pointer;">🖨️ Print Form</button>

    <div style="max-width: 1050px; margin: 0 auto; border: 1px solid #000; padding: 20px;">
        
        <table class="header-table">
            <tr>
                <td rowspan="3" style="width: 10%; text-align: center; vertical-align: middle;">
                    <img src="{logo2_b64}" width="60" height="60" alt="PNAC Logo" />
                </td>
                <td rowspan="3" style="width: 10%; text-align: center; vertical-align: middle;">
                    <img src="{logo1_b64}" width="60" height="60" alt="VAN Logo" />
                </td>
                <td rowspan="2" style="width: 60%; font-size: 16px; font-weight: bold;">
                    VITAL AGRI NUTRIENTS QC LAB<br/>
                    {title}
                </td>
                <td style="width: 20%; text-align: left; font-size: 10px;">
                    <strong>Format No:</strong> {format_no}
                </td>
            </tr>
            <tr>
                <td style="text-align: left; font-size: 10px;">
                    <strong>Revision No:</strong> {revision_no}
                </td>
            </tr>
            <tr>
                <td style="font-size: 11px; font-weight: bold;">
                    ISO/IEC 17025 Accredited
                </td>
                <td style="text-align: left; font-size: 10px;">
                    <strong>Page:</strong> 1 of 1
                </td>
            </tr>
        </table>

        <table class="main-table">
            <thead>
                <tr>
                    {table_headers}
                </tr>
            </thead>
            <tbody>
                {{% for item in {loop_var} %}}
                <tr>
                    <td style="width: 3%;">{{{{ forloop.counter }}}}</td>
                    {row_template}
                </tr>
                {{% endfor %}}
            </tbody>
        </table>

        <table style="width: 100%; border: none; margin-top: 40px; font-size: 12px; text-align: center;">
            <tr>
                <td>_________________________<br><strong>Prepared By (AQCM)</strong><br><br>Date:</td>
                <td>_________________________<br><strong>Reviewed By (QCM)</strong><br><br>Date:</td>
                <td>_________________________<br><strong>Approved By (CEO)</strong><br><br>Date:</td>
            </tr>
        </table>
        
    </div>
</body>
</html>
"""

# 1. Master List (4.02)
h_402 = "<th>Name of Equipment</th><th>Identification No.</th><th>Range</th><th>Location</th><th>Calibration Certificate No.</th><th>Calibration Certificate Date</th><th>Remarks</th>"
r_402 = """
<td>{{ item.name }}</td>
<td>{{ item.identification_no|default:"-" }}</td>
<td>{{ item.operating_range|default:"-" }}</td>
<td>{{ item.location|default:"-" }}</td>
<td>{{ item.calibrations.last.certificate_number|default:"-" }}</td>
<td>{{ item.calibrations.last.calibration_date|date:"d-M-Y"|default:"-" }}</td>
<td></td>
"""
with open(f"{template_dir}/equipment_master_list.html", "w") as f:
    f.write(get_base_html("MASTER LIST OF EQUIPMENTS", "QCL-FRM-4.02", "01", h_402, "equipments", r_402))

# 2. Calibration Program (4.04)
h_404 = "<th>Name of Equipment</th><th>Identification #</th><th>Location</th><th>Frequency of Calibration</th><th>Schedule for calibration (month)</th><th>Remarks</th>"
r_404 = """
<td>{{ item.name }}</td>
<td>{{ item.identification_no|default:"-" }}</td>
<td>{{ item.location|default:"-" }}</td>
<td>{{ item.calibration_frequency|default:"-" }}</td>
<td>{{ item.calibrations.last.next_due_date|date:"F Y"|default:"-" }}</td>
<td></td>
"""
with open(f"{template_dir}/calibration_program.html", "w") as f:
    f.write(get_base_html("CALIBRATION PROGRAM", "QCL-FRM-4.04", "01", h_404, "equipments", r_404))

# 3. Equipment Maintenance Record (4.03)
h_403 = "<th>Name of Equipment</th><th>Equipment Identification #</th><th>Make & Model / Serial Number</th><th>Location of Equipment</th><th>Maintenance Frequency</th><th>Maintenance Date</th><th>Parts Repaired/ Replaced</th><th>Maintenance By</th>"
r_403 = """
<td>{{ item.equipment.name }}</td>
<td>{{ item.equipment.identification_no|default:"-" }}</td>
<td>{{ item.equipment.manufacturer|default:"" }} {{ item.equipment.model_number|default:"" }} / {{ item.equipment.serial_number|default:"-" }}</td>
<td>{{ item.equipment.location|default:"-" }}</td>
<td>{{ item.equipment.maintenance_frequency|default:"-" }}</td>
<td>{{ item.maintenance_date|date:"d-M-Y" }}</td>
<td>{{ item.parts_repaired_replaced|default:"-" }}</td>
<td>{{ item.maintenance_by|default:"-" }}</td>
"""
with open(f"{template_dir}/equipment_maintenance_record.html", "w") as f:
    f.write(get_base_html("EQUIPMENT MAINTENANCE RECORD", "QCL-FRM-4.03", "01", h_403, "maintenances", r_403))

print("Templates for 4.02, 4.03, and 4.04 generated.")
