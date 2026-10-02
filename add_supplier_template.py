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
    <title>Supplier Evaluation Form</title>
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 12px; margin: 20px; }}
        .header-table {{ width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 20px; text-align: center; }}
        .header-table td {{ border: 1px solid #000; padding: 5px; }}
        
        .info-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        .info-table td {{ border: 1px solid #000; padding: 5px; }}
        
        .main-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13px; }}
        .main-table th, .main-table td {{ border: 1px solid #000; padding: 6px; }}
        .main-table th {{ background-color: #f2f2f2; text-align: center; }}
        
        .section-title {{ font-weight: bold; background-color: #e8e8e8; }}
        
        @media print {{
            button {{ display: none; }}
            body {{ margin: 0; }}
        }}
    </style>
</head>
<body>
    <button onclick="window.print()" style="padding: 10px 20px; margin-bottom: 20px; font-size: 14px; cursor: pointer;">🖨️ Print Form</button>

    {{% for s in suppliers %}}
    <div style="page-break-after: always; max-width: 800px; margin: 0 auto; border: 1px solid #000; padding: 20px;">
        
        <table class="header-table">
            <tr>
                <td rowspan="3" style="width: 15%; text-align: center; vertical-align: middle;">
                    <img src="{logo2_b64}" width="60" height="60" alt="PNAC Logo" />
                </td>
                <td rowspan="3" style="width: 15%; text-align: center; vertical-align: middle;">
                    <img src="{logo1_b64}" width="60" height="60" alt="VAN Logo" />
                </td>
                <td rowspan="2" style="width: 45%; font-size: 14px; font-weight: bold;">
                    VITAL AGRI NUTRIENTS QC LAB<br/>
                    External Provider Evaluation & Re-evaluation Form
                </td>
                <td style="width: 25%; text-align: left; font-size: 10px;">
                    <strong>Format No:</strong> QCL-FRM-6.03
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

        <div style="margin-bottom:10px;">
            <strong style="font-size:14px;">Section-A: General Evaluation</strong>
            <span style="float:right;">
                {{% if s.evaluation_type == 'NEW' %}} ☑ New Supplier &nbsp;&nbsp; ☐ Existing Provider {{% else %}} ☐ New Supplier &nbsp;&nbsp; ☑ Existing Provider {{% endif %}}
            </span>
        </div>

        <table class="info-table">
            <tr>
                <td width="30%"><strong>Supplier's Name</strong></td>
                <td colspan="3">{{{{ s.name }}}}</td>
            </tr>
            <tr>
                <td><strong>Contact Person</strong></td>
                <td colspan="3">{{{{ s.contact_person|default:"-" }}}}</td>
            </tr>
            <tr>
                <td><strong>Telephone #</strong></td>
                <td width="30%">{{{{ s.phone|default:"-" }}}}</td>
                <td width="15%"><strong>Email</strong></td>
                <td width="25%">{{{{ s.email|default:"-" }}}}</td>
            </tr>
        </table>

        <table class="main-table">
            <thead>
                <tr>
                    <th rowspan="2" colspan="2" style="width: 60%;">Technical Requirement</th>
                    <th colspan="4">Rating</th>
                </tr>
                <tr>
                    <th style="width: 10%;">Poor<br>(0)</th>
                    <th style="width: 10%;">Fair<br>(1)</th>
                    <th style="width: 10%;">Good<br>(2)</th>
                    <th style="width: 10%;">Excellence<br>(3)</th>
                </tr>
            </thead>
            <tbody>
                <!-- Row 1 -->
                <tr>
                    <td rowspan="2" style="font-weight:bold; width: 25%;">Market Feedback</td>
                    <td>Image and reputation</td>
                    <td style="text-align:center;">{{% if s.score_market_image == 0 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_market_image == 1 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_market_image == 2 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_market_image == 3 %}}☑{{% else %}}☐{{% endif %}}</td>
                </tr>
                <tr>
                    <td>Market share</td>
                    <td style="text-align:center;">{{% if s.score_market_share == 0 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_market_share == 1 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_market_share == 2 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_market_share == 3 %}}☑{{% else %}}☐{{% endif %}}</td>
                </tr>
                <!-- Row 3 -->
                <tr>
                    <td rowspan="5" style="font-weight:bold;">Operational Performance</td>
                    <td>Technical Capacity*</td>
                    <td style="text-align:center;">{{% if s.score_technical_capacity == 0 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_technical_capacity == 1 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_technical_capacity == 2 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_technical_capacity == 3 %}}☑{{% else %}}☐{{% endif %}}</td>
                </tr>
                <tr>
                    <td>Lead Time</td>
                    <td style="text-align:center;">{{% if s.score_lead_time == 0 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_lead_time == 1 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_lead_time == 2 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_lead_time == 3 %}}☑{{% else %}}☐{{% endif %}}</td>
                </tr>
                <tr>
                    <td>Product Quality/Services</td>
                    <td style="text-align:center;">{{% if s.score_product_quality == 0 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_product_quality == 1 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_product_quality == 2 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_product_quality == 3 %}}☑{{% else %}}☐{{% endif %}}</td>
                </tr>
                <tr>
                    <td>Order Processing</td>
                    <td style="text-align:center;">{{% if s.score_order_processing == 0 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_order_processing == 1 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_order_processing == 2 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_order_processing == 3 %}}☑{{% else %}}☐{{% endif %}}</td>
                </tr>
                <tr>
                    <td>Fulfill Technical Requirement</td>
                    <td style="text-align:center;">{{% if s.score_fulfill_requirements == 0 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_fulfill_requirements == 1 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_fulfill_requirements == 2 %}}☑{{% else %}}☐{{% endif %}}</td>
                    <td style="text-align:center;">{{% if s.score_fulfill_requirements == 3 %}}☑{{% else %}}☐{{% endif %}}</td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align:right; font-weight:bold;">Total Score Achieved:</td>
                    <td colspan="4" style="text-align:center; font-weight:bold; font-size:14px;">{{{{ s.total_score }}}} / 21</td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align:right; font-weight:bold;">Grading:</td>
                    <td colspan="4" style="text-align:center;">
                        <strong>{{{{ s.grading }}}}</strong> 
                        <span style="font-size:10px;">(Poor:0-6 | Fair:7-12 | Good:13-18 | Excellence:19-21)</span>
                    </td>
                </tr>
            </tbody>
        </table>

        <div style="font-size: 11px; margin-bottom: 10px;">
            <em>*In case of supplies and service provider</em>
        </div>

        <table class="info-table" style="margin-bottom: 20px;">
            <tr>
                <td style="width: 50%;">Has sample of product/services been approved by QC section?</td>
                <td style="width: 50%; font-weight:bold;">
                    {{% if s.sample_approved_by_qc == 'YES' %}}☑ Yes &nbsp;&nbsp; ☐ No &nbsp;&nbsp; ☐ N/A
                    {{% elif s.sample_approved_by_qc == 'NO' %}}☐ Yes &nbsp;&nbsp; ☑ No &nbsp;&nbsp; ☐ N/A
                    {{% else %}}☐ Yes &nbsp;&nbsp; ☐ No &nbsp;&nbsp; ☑ N/A{{% endif %}}
                </td>
            </tr>
        </table>

        <div style="margin-bottom:5px;">
            <strong style="font-size:14px;">Section-C: Approval</strong>
        </div>
        <table class="info-table">
            <tr>
                <td style="width: 25%;"><strong>Decision</strong></td>
                <td colspan="3" style="font-weight:bold;">
                    {{% if s.decision == 'APPROVED' %}}☑ Approved &nbsp;&nbsp; ☐ Rejected &nbsp;&nbsp; ☐ Continue
                    {{% elif s.decision == 'REJECTED' %}}☐ Approved &nbsp;&nbsp; ☑ Rejected &nbsp;&nbsp; ☐ Continue
                    {{% else %}}☐ Approved &nbsp;&nbsp; ☐ Rejected &nbsp;&nbsp; ☑ Continue{{% endif %}}
                </td>
            </tr>
            <tr>
                <td><strong>Remarks (If any)</strong></td>
                <td colspan="3">{{{{ s.remarks|default:"" }}}}</td>
            </tr>
            <tr>
                <td><strong>Evaluated By</strong></td>
                <td style="width: 35%;">___________________</td>
                <td style="width: 15%;"><strong>Date</strong></td>
                <td style="width: 25%;">{{{{ s.last_evaluation_date|date:"d-M-Y"|default:"___/___/_____" }}}}</td>
            </tr>
            <tr>
                <td><strong>Approved By</strong></td>
                <td>___________________</td>
                <td><strong>Date</strong></td>
                <td>___/___/_____</td>
            </tr>
        </table>
        
    </div>
    {{% endfor %}}
</body>
</html>
"""

with open(f"{template_dir}/supplier_evaluation.html", 'w') as f:
    f.write(template_html)

print("Generated Supplier Evaluation template.")
