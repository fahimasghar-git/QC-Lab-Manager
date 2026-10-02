import re
import os

comp_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/competency_report.html'
with open(comp_path, 'r') as f:
    comp_content = f.read()

imgs = re.findall(r'<img src="(data:image/[^"]+)"', comp_content)
logo2_b64 = imgs[0] if len(imgs) > 0 else ""
logo1_b64 = imgs[1] if len(imgs) > 1 else ""

template_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/templates/management'
os.makedirs(template_dir, exist_ok=True)

template_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Non Conformance Form</title>
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 13px; margin: 20px; }}
        .header-table {{ width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 20px; text-align: center; }}
        .header-table td {{ border: 1px solid #000; padding: 5px; }}
        
        .main-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        .main-table td, .main-table th {{ border: 1px solid #000; padding: 8px; vertical-align: top; }}
        .section-header {{ background-color: #f2f2f2; font-weight: bold; text-align: center; }}
        
        @media print {{
            button {{ display: none; }}
            body {{ margin: 0; }}
        }}
    </style>
</head>
<body>
    <button onclick="window.print()" style="padding: 10px 20px; margin-bottom: 20px; font-size: 14px; cursor: pointer;">🖨️ Print Form</button>

    {{% for nc in ncs %}}
    <div style="page-break-after: always; max-width: 800px; margin: 0 auto; border: 1px solid #000; padding: 20px;">
        
        <!-- MASTER DOCUMENT CONTROL HEADER -->
        <table class="header-table">
            <tr>
                <td rowspan="3" style="width: 15%; text-align: center; vertical-align: middle;">
                    <img src="{logo2_b64}" width="60" height="60" alt="PNAC Logo" />
                </td>
                <td rowspan="3" style="width: 15%; text-align: center; vertical-align: middle;">
                    <img src="{logo1_b64}" width="60" height="60" alt="VAN Logo" />
                </td>
                <td rowspan="2" style="width: 45%; font-size: 16px; font-weight: bold;">
                    VITAL AGRI NUTRIENTS QC LAB<br/>
                    Non Conformance Form
                </td>
                <td style="width: 25%; text-align: left; font-size: 10px;">
                    <strong>Format No:</strong> QCL-FRM-14.01
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

        <div style="margin-bottom: 10px;">
            <strong>Ref. No:</strong> {{{{ nc.nc_id }}}} <span style="float:right;"><strong>Date:</strong> {{{{ nc.date_identified|date:"d/m/Y" }}}}</span>
        </div>
        
        <table class="main-table">
            <tr>
                <td colspan="4" class="section-header">SOURCE OF NON-CONFORMANCE</td>
            </tr>
            <tr>
                <td colspan="4">
                    {{% if nc.source == 'AUDIT' %}}☑{{% else %}}☐{{% endif %}} Audit NC &nbsp;&nbsp;&nbsp;
                    {{% if nc.source == 'LAB' %}}☑{{% else %}}☐{{% endif %}} Laboratory Activities &nbsp;&nbsp;&nbsp;
                    {{% if nc.source == 'SUGGESTION' %}}☑{{% else %}}☐{{% endif %}} Suggestion &nbsp;&nbsp;&nbsp;
                    {{% if nc.source == 'PT_ILC' %}}☑{{% else %}}☐{{% endif %}} PT/ILC &nbsp;&nbsp;&nbsp;
                    {{% if nc.source == 'COMPLAINT' %}}☑{{% else %}}☐{{% endif %}} Complaint &nbsp;&nbsp;&nbsp;
                    {{% if nc.source == 'FEEDBACK' %}}☑{{% else %}}☐{{% endif %}} Customer Feedback<br><br>
                    {{% if nc.source == 'RISK' %}}☑{{% else %}}☐{{% endif %}} Risk Assessment &nbsp;&nbsp;&nbsp;
                    {{% if nc.source == 'OTHER' %}}☑{{% else %}}☐{{% endif %}} Any Other: __________________
                </td>
            </tr>
            <tr>
                <td colspan="4" style="height: 100px;">
                    <strong>Description of Non-conformance:</strong><br>
                    {{{{ nc.description|default:"" }}}}
                </td>
            </tr>
            <tr>
                <td colspan="4" class="section-header">REVIEW</td>
            </tr>
            <tr>
                <td width="25%"><strong>Impact on Previous Result:</strong></td>
                <td width="25%">{{% if nc.impact_on_previous_result %}}☑ Yes &nbsp; ☐ No{{% else %}}☐ Yes &nbsp; ☑ No{{% endif %}}</td>
                <td width="25%"><strong>Level of Risk:</strong></td>
                <td width="25%">
                    {{% if nc.level_of_risk == 'VERY_LOW' %}}☑{{% else %}}☐{{% endif %}} Very Low<br>
                    {{% if nc.level_of_risk == 'LOW' %}}☑{{% else %}}☐{{% endif %}} Low<br>
                    {{% if nc.level_of_risk == 'MODERATE' %}}☑{{% else %}}☐{{% endif %}} Moderate<br>
                    {{% if nc.level_of_risk == 'HIGH' %}}☑{{% else %}}☐{{% endif %}} High<br>
                    {{% if nc.level_of_risk == 'VERY_HIGH' %}}☑{{% else %}}☐{{% endif %}} Very High
                </td>
            </tr>
            <tr>
                <td><strong>Type of Non-conforming Work:</strong></td>
                <td>{{% if nc.nc_type == 'ESSENTIAL' %}}☑ Essential &nbsp; ☐ Minor{{% else %}}☐ Essential &nbsp; ☑ Minor{{% endif %}}</td>
                <td><strong>Acceptance:</strong></td>
                <td>
                    {{% if nc.acceptance_status == 'ACCEPTED' %}}☑{{% else %}}☐{{% endif %}} Accepted<br>
                    {{% if nc.acceptance_status == 'REJECTED' %}}☑{{% else %}}☐{{% endif %}} Rejected
                </td>
            </tr>
            <tr>
                <td><strong>Withhold Reports:</strong></td>
                <td>{{% if nc.withhold_reports %}}☑ Yes &nbsp; ☐ No{{% else %}}☐ Yes &nbsp; ☑ No{{% endif %}}</td>
                <td><strong>Halt work / Recall work:</strong></td>
                <td>
                    {{% if nc.halt_work %}}☑{{% else %}}☐{{% endif %}} Halt work<br>
                    {{% if nc.recall_work %}}☑{{% else %}}☐{{% endif %}} Recall work
                </td>
            </tr>
            <tr>
                <td colspan="2"><strong>Reviewed By (AQCM):</strong> {{{{ nc.reviewed_by.get_full_name|default:"___________________" }}}}</td>
                <td colspan="2"><strong>Evaluated By (QCM):</strong> {{{{ nc.evaluated_by.get_full_name|default:"___________________" }}}}</td>
            </tr>
            <tr>
                <td colspan="4" class="section-header">ROOT CAUSE ANALYSIS</td>
            </tr>
            <tr>
                <td colspan="4" style="height: 80px;">{{{{ nc.root_cause_analysis|default:"" }}}}</td>
            </tr>
            <tr>
                <td colspan="4" class="section-header">CORRECTIVE & PREVENTIVE ACTION</td>
            </tr>
            <tr>
                <td colspan="4" style="height: 80px;"><strong>Corrective Action:</strong><br>{{{{ nc.corrective_action|default:"" }}}}<br><br><strong>Preventive Action:</strong><br>{{{{ nc.preventive_action|default:"" }}}}</td>
            </tr>
            <tr>
                <td colspan="4" class="section-header">STATUS / VERIFICATION OF EFFECTIVENESS</td>
            </tr>
            <tr>
                <td colspan="4" style="height: 60px;">
                    <strong>Status:</strong> {{{{ nc.get_status_display }}}}<br>
                    {{{{ nc.verification_notes|default:"" }}}}
                </td>
            </tr>
            <tr>
                <td colspan="2"><strong>Closed By (QCM):</strong> {{{{ nc.closed_by.get_full_name|default:"___________________" }}}}</td>
                <td colspan="2"><strong>Date Closed:</strong> {{{{ nc.closed_date|date:"d/m/Y"|default:"___/___/_____" }}}}</td>
            </tr>
        </table>
        
    </div>
    {{% endfor %}}
</body>
</html>
"""

with open(f"{template_dir}/non_conformance_form.html", 'w') as f:
    f.write(template_html)

print("Generated NC template.")
