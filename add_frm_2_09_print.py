import re
import os

# Extract base64 logos from the other competency report
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
    <title>Evaluation of Competency</title>
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 12px; margin: 20px; }}
        .header-table {{ width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 20px; text-align: center; }}
        .header-table td {{ border: 1px solid #000; padding: 5px; }}
        
        .main-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13px; }}
        .main-table th, .main-table td {{ border: 1px solid #000; padding: 8px; text-align: left; vertical-align: top; }}
        .main-table th {{ background-color: #f2f2f2; }}
        
        .section-title {{ font-weight: bold; background-color: #e8e8e8; }}
        
        @media print {{
            button {{ display: none; }}
            body {{ margin: 0; }}
        }}
    </style>
</head>
<body>
    <button onclick="window.print()" style="padding: 10px 20px; margin-bottom: 20px; font-size: 14px; cursor: pointer;">🖨️ Print Form</button>

    {{% for eval in evaluations %}}
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
                    Evaluation of Competency
                </td>
                <td style="width: 25%; text-align: left; font-size: 10px;">
                    <strong>Format No:</strong> QCL-FRM-2.09
                </td>
            </tr>
            <tr>
                <td style="text-align: left; font-size: 10px;">
                    <strong>Revision No:</strong> 00
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

        <!-- Section A -->
        <table class="main-table">
            <tr>
                <td colspan="4" class="section-title">Section A: Basic Information</td>
            </tr>
            <tr>
                <td width="25%"><strong>Name of Lab Personnel</strong></td>
                <td width="25%">{{{{ eval.analyst.get_full_name|default:eval.analyst.username }}}}</td>
                <td width="25%"><strong>Date of Supervision</strong></td>
                <td width="25%">{{{{ eval.evaluation_date|date:"d-M-Y" }}}}</td>
            </tr>
            <tr>
                <td><strong>Supervisor / Evaluator</strong></td>
                <td colspan="3">{{{{ eval.supervisor.get_full_name|default:eval.supervisor.username }}}}</td>
            </tr>
        </table>

        <!-- Section B -->
        <table class="main-table">
            <tr>
                <td colspan="2" class="section-title">Section B: Evaluation Scale Key</td>
            </tr>
            <tr><td width="5%"><strong>ND</strong></td><td><strong>Needs Development</strong> Lacks Basics: Needs continuous training and supervision</td></tr>
            <tr><td><strong>AC</strong></td><td><strong>Approaching Competence</strong> Can Work Under Supervision: Needs close supervision</td></tr>
            <tr><td><strong>C</strong></td><td><strong>Competent</strong> Can Work Independently: Competent to perform lab activities</td></tr>
            <tr><td><strong>HC</strong></td><td><strong>Highly Competent</strong> Can Supervise: Highly competent and can supervise Lab activities</td></tr>
            <tr><td><strong>E</strong></td><td><strong>Exceptional</strong> Hold Full Command on the subjects: Can perform, supervise, handles complex matters related to lab activities...</td></tr>
        </table>

        <!-- Section C -->
        <table class="main-table">
            <thead>
                <tr>
                    <th colspan="3" class="section-title">Section C: Evaluation Description</th>
                </tr>
                <tr>
                    <th width="40%">Competency Parameters</th>
                    <th width="20%" style="text-align: center;">Evaluation Scale</th>
                    <th width="40%">Remarks / Comments</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Analysis Skills</td>
                    <td style="text-align: center; font-weight: bold;">{{{{ eval.score_analysis_skills }}}}</td>
                    <td rowspan="5" style="vertical-align: top;">{{{{ eval.remarks|default:"" }}}}</td>
                </tr>
                <tr>
                    <td>Lab Equipment Handling</td>
                    <td style="text-align: center; font-weight: bold;">{{{{ eval.score_equipment_handling }}}}</td>
                </tr>
                <tr>
                    <td>Awareness ISO 17025: 2023</td>
                    <td style="text-align: center; font-weight: bold;">{{{{ eval.score_iso_awareness }}}}</td>
                </tr>
                <tr>
                    <td>Testing Skills</td>
                    <td style="text-align: center; font-weight: bold;">{{{{ eval.score_testing_skills }}}}</td>
                </tr>
                <tr>
                    <td>Sample preparation skills</td>
                    <td style="text-align: center; font-weight: bold;">{{{{ eval.score_sample_prep }}}}</td>
                </tr>
            </tbody>
        </table>

        <div style="font-size: 11px; margin-bottom: 30px;">
            <em>If lab personnel lie on ND scale in any parameter, then training is to be given on that competency parameter.</em>
        </div>

        <table style="width: 100%; border: none; margin-top: 40px; font-size: 14px;">
            <tr>
                <td style="text-align: right; width: 100%;">_________________________<br><strong>Manager QC</strong></td>
            </tr>
        </table>
        
    </div>
    {{% endfor %}}
</body>
</html>
"""

with open(f"{template_dir}/competency_evaluation_report.html", 'w') as f:
    f.write(template_html)

print("QCL-FRM-2.09 template generated.")
