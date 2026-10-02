import re
import os

# 1. Add action to admin.py
admin_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/admin.py'
with open(admin_path, 'r') as f:
    content = f.read()

# Add imports for printing if not there
if "from django.shortcuts import render" not in content:
    content = content.replace("from django.contrib import admin", "from django.contrib import admin\nfrom django.shortcuts import render")

# Define the action
action_code = """
@admin.action(description='🖨️ Print Competency Report (QCL-FRM-1.04)')
def print_competency_report(modeladmin, request, queryset):
    return render(request, 'resources/competency_report.html', {'records': queryset})

"""

# Insert action before CompetencyRecordAdmin
content = content.replace("@admin.register(CompetencyRecord)", action_code + "@admin.register(CompetencyRecord)")

# Add action to the class
class_str = """class CompetencyRecordAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('analyst', 'competency_level', 'total_score', 'status', 'training_date')
    list_filter = ('status', 'analyst')
    search_fields = ('analyst__username', 'test_method__name')
    readonly_fields = ('total_score', 'competency_level')
    actions = [print_competency_report]"""

content = re.sub(r'class CompetencyRecordAdmin\(ModelAdmin, SimpleHistoryAdmin\):\n.*?readonly_fields = .*?\n', class_str + "\n", content, flags=re.DOTALL)

with open(admin_path, 'w') as f:
    f.write(content)


# 2. Extract base64 logos from analysis_request
ar_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/analysis_request.html'
with open(ar_path, 'r') as f:
    ar_content = f.read()

# We can regex match the src attributes for the images
imgs = re.findall(r'<img src="(data:image/[^"]+)"', ar_content)
logo2_b64 = imgs[0] if len(imgs) > 0 else ""
logo1_b64 = imgs[1] if len(imgs) > 1 else ""

# 3. Create the template
template_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources'
os.makedirs(template_dir, exist_ok=True)

template_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Competency Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 12px; margin: 20px; }}
        .header-table {{ width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 20px; text-align: center; }}
        .header-table td {{ border: 1px solid #000; padding: 5px; }}
        
        .info-table {{ width: 100%; border: none; font-size: 14px; margin-bottom: 20px; }}
        .info-table td {{ padding: 5px; }}
        
        .main-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13px; }}
        .main-table th, .main-table td {{ border: 1px solid #000; padding: 8px; text-align: left; vertical-align: top; }}
        .main-table th {{ background-color: #f2f2f2; }}
        
        .scale-info {{ font-size: 12px; line-height: 1.6; margin-bottom: 40px; }}
        .signatures {{ width: 100%; margin-top: 50px; text-align: center; font-size: 12px; }}
        
        @media print {{
            button {{ display: none; }}
            body {{ margin: 0; }}
        }}
    </style>
</head>
<body>
    <button onclick="window.print()" style="padding: 10px 20px; margin-bottom: 20px; font-size: 14px; cursor: pointer;">🖨️ Print Form</button>

    {{% for record in records %}}
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
                    Competency Monitoring of Laboratory Personnel
                </td>
                <td style="width: 25%; text-align: left; font-size: 10px;">
                    <strong>Format No:</strong> QCL-FRM-1.04
                </td>
            </tr>
            <tr>
                <td style="text-align: left; font-size: 10px;">
                    <strong>Revision No:</strong> 02
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

        <table class="info-table">
            <tr>
                <td width="20%"><strong>Name of Employee:</strong></td>
                <td width="30%" style="border-bottom: 1px solid #000;">{{{{ record.analyst.get_full_name|default:record.analyst.username }}}}</td>
                <td width="15%"><strong>Designation:</strong></td>
                <td width="35%" style="border-bottom: 1px solid #000;">Assistant Analyst / Analyst</td>
            </tr>
            <tr>
                <td><strong>Main Functions:</strong></td>
                <td colspan="3" style="border-bottom: 1px solid #000;">Performing Laboratory Activities</td>
            </tr>
        </table>

        <table class="main-table">
            <thead>
                <tr>
                    <th width="35%">Necessary Competence Requirements</th>
                    <th width="15%">Competence Score</th>
                    <th width="50%">Remarks (where necessary)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Education</strong></td>
                    <td style="text-align: center; font-weight: bold;">{{{{ record.score_education }}}}</td>
                    <td></td>
                </tr>
                <tr>
                    <td><strong>Qualification</strong></td>
                    <td style="text-align: center; font-weight: bold;">{{{{ record.score_qualification }}}}</td>
                    <td></td>
                </tr>
                <tr>
                    <td><strong>Experience</strong></td>
                    <td style="text-align: center; font-weight: bold;">{{{{ record.score_experience }}}}</td>
                    <td></td>
                </tr>
                <tr>
                    <td><strong>Training</strong><br><span style="font-size: 10px; font-weight: normal;">ISO 17025, GDP, Method Auth</span></td>
                    <td style="text-align: center; font-weight: bold;">{{{{ record.score_training }}}}</td>
                    <td>{{{{ record.notes|default:"" }}}}</td>
                </tr>
                <tr>
                    <td><strong>Technical Knowledge</strong><br><span style="font-size: 10px; font-weight: normal;">Testing, ISO, Equipment</span></td>
                    <td style="text-align: center; font-weight: bold;">{{{{ record.score_technical_knowledge }}}}</td>
                    <td></td>
                </tr>
                <tr>
                    <td><strong>Skills</strong><br><span style="font-size: 10px; font-weight: normal;">Instrument handling, Troubleshooting</span></td>
                    <td style="text-align: center; font-weight: bold;">{{{{ record.score_skills }}}}</td>
                    <td></td>
                </tr>
                <tr>
                    <td><strong>Challenge Testing</strong><br><span style="font-size: 10px; font-weight: normal;">Blind samples, Complaints</span></td>
                    <td style="text-align: center; font-weight: bold;">{{{{ record.score_challenge_testing }}}}</td>
                    <td></td>
                </tr>
                <tr>
                    <td><strong>Proficiency Testing</strong><br><span style="font-size: 10px; font-weight: normal;">Ability to perform PT</span></td>
                    <td style="text-align: center; font-weight: bold;">{{{{ record.score_proficiency_testing }}}}</td>
                    <td></td>
                </tr>
                <tr>
                    <td style="text-align: right;"><strong>Total Average Score:</strong></td>
                    <td colspan="2" style="font-weight: bold;">{{{{ record.total_score }}}} / 32 ({{{{ record.competency_level }}}})</td>
                </tr>
            </tbody>
        </table>

        <div class="scale-info">
            <strong>4 = High Competence (Level 3)</strong> (Completes task independently)<br>
            <strong>3 = Partial Competence (Level 2)</strong> (Need occasional support)<br>
            <strong>2 = Low Competence (Level 1)</strong> (Needs ongoing support)<br>
            <strong>1 = No Competence (Level 0)</strong> (Needs Training & direction)
        </div>

        <table style="width: 100%; border: none; margin-top: 40px; font-size: 14px;">
            <tr>
                <td style="text-align: left; width: 33%;">_________________________<br><strong>Prepared By</strong></td>
                <td style="text-align: center; width: 33%;">_________________________<br><strong>Checked By</strong></td>
                <td style="text-align: right; width: 33%;">_________________________<br><strong>Approved By</strong></td>
            </tr>
        </table>
        
    </div>
    {{% endfor %}}
</body>
</html>
"""

with open(f"{template_dir}/competency_report.html", 'w') as f:
    f.write(template_html)

print("Competency print view added")
