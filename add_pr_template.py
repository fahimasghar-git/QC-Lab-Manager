import re
import os

comp_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/competency_report.html'
with open(comp_path, 'r') as f:
    comp_content = f.read()

imgs = re.findall(r'<img src="(data:image/[^"]+)"', comp_content)
logo2_b64 = imgs[0] if len(imgs) > 0 else ""
logo1_b64 = imgs[1] if len(imgs) > 1 else ""

template_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources'

template_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Store Purchase Demand</title>
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 11px; margin: 20px; }}
        @page {{ size: landscape; }}
        .header-table {{ width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 20px; text-align: center; }}
        .header-table td {{ border: 1px solid #000; padding: 5px; }}
        
        .main-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 11px; }}
        .main-table th, .main-table td {{ border: 1px solid #000; padding: 6px; text-align: center; vertical-align: middle; }}
        .main-table th {{ background-color: #f2f2f2; font-weight: bold; }}
        
        .top-info {{ width: 100%; margin-bottom: 10px; font-size: 12px; }}
        .top-info td {{ padding: 4px; }}
        
        @media print {{
            button {{ display: none; }}
            body {{ margin: 0; }}
        }}
    </style>
</head>
<body>
    <button onclick="window.print()" style="padding: 10px 20px; margin-bottom: 20px; font-size: 14px; cursor: pointer;">🖨️ Print Form</button>

    <div style="max-width: 1050px; margin: 0 auto; border: 1px solid #000; padding: 20px;">
        
        <!-- MASTER DOCUMENT CONTROL HEADER -->
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
                    STORE PURCHASE DEMAND
                </td>
                <td style="width: 20%; text-align: left; font-size: 10px;">
                    <strong>Format No:</strong> QCL-FRM-6.07
                </td>
            </tr>
            <tr>
                <td style="text-align: left; font-size: 10px;">
                    <strong>Revision No:</strong> 01
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
        
        <table class="top-info">
            <tr>
                <td style="width: 50%;"><strong>SPD No:</strong> _______________________</td>
                <td style="width: 50%; text-align: right;"><strong>Date:</strong> _______________________</td>
            </tr>
            <tr>
                <td style="width: 50%;"><strong>Insp Mints NO & Date:</strong> _______________________</td>
                <td style="width: 50%; text-align: right;"><strong>Service Call No & Date:</strong> _______________________</td>
            </tr>
            <tr>
                <td colspan="2"><strong>Section:</strong> QC Laboratory</td>
            </tr>
        </table>

        <table class="main-table">
            <thead>
                <tr>
                    <th rowspan="2" style="width: 4%;">S.No</th>
                    <th rowspan="2" style="width: 20%;">Items</th>
                    <th colspan="4" style="width: 36%;">Complete Specification</th>
                    <th rowspan="2" style="width: 8%;">Quantity<br>Required</th>
                    <th rowspan="2" style="width: 8%;">Stock in<br>Hand</th>
                    <th rowspan="2" style="width: 8%;">Net Purchase<br>Required</th>
                    <th rowspan="2" style="width: 16%;">Purpose of<br>Purchase</th>
                </tr>
                <tr>
                    <th style="font-size: 10px;">Model</th>
                    <th style="font-size: 10px;">Brand</th>
                    <th style="font-size: 10px;">Quality</th>
                    <th style="font-size: 10px;">Capacity</th>
                </tr>
            </thead>
            <tbody>
                {{% for item in requests %}}
                <tr>
                    <td>{{{{ forloop.counter }}}}</td>
                    <td style="text-align: left;">{{{{ item.item_description }}}}</td>
                    <td colspan="4">{{{{ item.specification|default:"-" }}}}</td>
                    <td>{{{{ item.quantity_required }}}}</td>
                    <td>{{{{ item.stock_in_hand }}}}</td>
                    <td>{{{{ item.net_purchase_required }}}}</td>
                    <td>{{{{ item.purpose|default:"-" }}}}</td>
                </tr>
                {{% endfor %}}
                
                {{% if requests|length < 5 %}}
                <!-- Fill empty rows if there are few items -->
                <tr><td>&nbsp;</td><td></td><td colspan="4"></td><td></td><td></td><td></td><td></td></tr>
                <tr><td>&nbsp;</td><td></td><td colspan="4"></td><td></td><td></td><td></td><td></td></tr>
                <tr><td>&nbsp;</td><td></td><td colspan="4"></td><td></td><td></td><td></td><td></td></tr>
                {{% endif %}}
            </tbody>
        </table>

        <table style="width: 100%; border: none; margin-top: 60px; font-size: 12px; text-align: center;">
            <tr>
                <td>_________________________<br><strong>Indentor</strong></td>
                <td>_________________________<br><strong>Store Keeper</strong></td>
                <td>_________________________<br><strong>Plant Manager</strong></td>
            </tr>
        </table>
        
    </div>
</body>
</html>
"""

with open(f"{template_dir}/store_purchase_demand.html", 'w') as f:
    f.write(template_html)

print("Generated PR template.")
