import os

def write_template(path, title, form_no, landscape, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    orientation = "landscape" if landscape else "portrait"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QCL-FRM-{form_no} {title}</title>
    <style>
        @page {{
            size: A4 {orientation};
            margin: 1.5cm;
            @frame header_frame {{
                -pdf-frame-content: header_content;
                top: 1.5cm; left: 1.5cm; right: 1.5cm; height: 3cm;
            }}
            @frame footer_frame {{
                -pdf-frame-content: footer_content;
                bottom: 1cm; left: 1.5cm; right: 1.5cm; height: 1cm;
            }}
        }}
        body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11px; color: #333; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 15px; }}
        th, td {{ border: 1px solid #000; padding: 5px; vertical-align: middle; }}
        th {{ background-color: #d9d9d9; font-weight: bold; text-align: center; }}
        .header-table th, .header-table td {{ text-align: center; vertical-align: middle; font-size: 12px; background-color: #fff; }}
        .noborder {{ border: none; }}
        .noborder td {{ border: none; }}
    </style>
</head>
<body>
    <div id="header_content">
        <table class="header-table">
            <tr>
                <td rowspan="3" style="width: 20%;">
                    <img src="{{{{ request.scheme }}}}://{{{{ request.get_host }}}}/static/images/logo.png" style="height: 50px;" alt="Logo" />
                </td>
                <td rowspan="3" style="width: 50%; font-size: 16px; font-weight: bold;">
                    {title.upper()}
                </td>
                <td style="width: 30%; text-align: left;"><strong>Format No.:</strong> QCL-FRM-{form_no}</td>
            </tr>
            <tr><td style="text-align: left;"><strong>Issue Date:</strong> 15-01-2024</td></tr>
            <tr><td style="text-align: left;"><strong>Revision No.:</strong> 01</td></tr>
        </table>
    </div>
    <div id="footer_content" style="text-align: right; font-size: 10px;">
        Page <pdf:pagenumber> of <pdf:pagecount>
    </div>
    {content}
</body>
</html>"""
    with open(path, 'w') as f:
        f.write(html)
    print(f"Created {path}")

# 20.01 Master List Records
write_template(
    'management/templates/management/master_list_records.html',
    'Master List of Records', '20.01', True,
    """
    <table>
        <thead>
            <tr>
                <th>Sr. No</th>
                <th>Record Title</th>
                <th>Record Code</th>
                <th>Revision No.</th>
                <th>File code</th>
                <th>File Location</th>
                <th>Retention Period</th>
                <th>Remarks</th>
            </tr>
        </thead>
        <tbody>
            {% for rec in records %}
            <tr>
                <td style="text-align: center;">{{ forloop.counter }}</td>
                <td>{{ rec.title }}</td>
                <td style="text-align: center;">{{ rec.code }}</td>
                <td style="text-align: center;">{{ rec.revision_no }}</td>
                <td style="text-align: center;">{{ rec.file_code }}</td>
                <td>{{ rec.location }}</td>
                <td style="text-align: center;">{{ rec.retention_period }}</td>
                <td>{{ rec.remarks|default:"" }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="8" style="text-align: center;">No records found.</td></tr>
            {% endfor %}
        </tbody>
    </table>
    <table class="noborder" style="margin-top: 50px;">
        <tr>
            <td style="width: 33%; text-align: center;">______________________<br/><br/>Prepared By</td>
            <td style="width: 33%; text-align: center;">______________________<br/><br/>Reviewed By</td>
            <td style="width: 33%; text-align: center;">______________________<br/><br/>Approved By</td>
        </tr>
    </table>
    """
)

# 20.02 Master List Files
write_template(
    'management/templates/management/master_list_files.html',
    'Master List of Files and Folders', '20.02', True,
    """
    <table>
        <thead>
            <tr>
                <th>S #</th>
                <th>File code</th>
                <th>Title of File/Folder/Register</th>
                <th>Volume</th>
                <th>Keeper</th>
                <th>Location</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for f in files %}
            <tr>
                <td style="text-align: center;">{{ forloop.counter }}</td>
                <td style="text-align: center;">{{ f.file_code }}</td>
                <td>{{ f.title }}</td>
                <td style="text-align: center;">{{ f.volume }}</td>
                <td style="text-align: center;">{{ f.keeper }}</td>
                <td>{{ f.location }}</td>
                <td style="text-align: center;">{{ f.status }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="7" style="text-align: center;">No files found.</td></tr>
            {% endfor %}
        </tbody>
    </table>
    <table class="noborder" style="margin-top: 50px;">
        <tr>
            <td style="width: 33%; text-align: center;">______________________<br/><br/>Prepared By</td>
            <td style="width: 33%; text-align: center;">______________________<br/><br/>Reviewed By</td>
            <td style="width: 33%; text-align: center;">______________________<br/><br/>Approved By</td>
        </tr>
    </table>
    """
)

# 21.01 Customer Feedback
write_template(
    'management/templates/management/customer_feedback.html',
    'Customer Feed back', '21.01', False,
    """
    {% for fb in feedbacks %}
    <table class="noborder">
        <tr>
            <td style="width: 20%; font-weight: bold;">Customer Name:</td>
            <td style="width: 80%; text-decoration: underline;">{{ fb.customer_name }}</td>
        </tr>
        <tr>
            <td style="width: 20%; font-weight: bold;">Date:</td>
            <td style="width: 80%; text-decoration: underline;">{{ fb.date|date:"d-m-Y" }}</td>
        </tr>
    </table>
    
    <table>
        <thead>
            <tr>
                <th rowspan="2" style="width: 5%;">Sr. #</th>
                <th rowspan="2" style="width: 55%;">Description</th>
                <th colspan="4" style="width: 40%;">Scale</th>
            </tr>
            <tr>
                <th>Excellent A+ (4)</th>
                <th>V. Good A (3)</th>
                <th>Good B (2)</th>
                <th>Poor C (1)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center;">1</td>
                <td>How do you estimate time of delivery of our laboratory reports?</td>
                <td style="text-align: center;">{% if fb.q1_delivery_time == 4 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q1_delivery_time == 3 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q1_delivery_time == 2 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q1_delivery_time == 1 %}✓{% endif %}</td>
            </tr>
            <tr>
                <td style="text-align: center;">2</td>
                <td>How do you estimate politeness of our laboratory staff?</td>
                <td style="text-align: center;">{% if fb.q2_politeness == 4 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q2_politeness == 3 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q2_politeness == 2 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q2_politeness == 1 %}✓{% endif %}</td>
            </tr>
            <tr>
                <td style="text-align: center;">3</td>
                <td>How do you estimate accuracy of contents of our Laboratory reports?</td>
                <td style="text-align: center;">{% if fb.q3_accuracy == 4 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q3_accuracy == 3 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q3_accuracy == 2 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q3_accuracy == 1 %}✓{% endif %}</td>
            </tr>
            <tr>
                <td style="text-align: center;">4</td>
                <td>How do you rate our response to your complaints & feedbacks?</td>
                <td style="text-align: center;">{% if fb.q4_response == 4 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q4_response == 3 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q4_response == 2 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q4_response == 1 %}✓{% endif %}</td>
            </tr>
            <tr>
                <td style="text-align: center;">5</td>
                <td>Rating of your overall satisfaction level?</td>
                <td style="text-align: center;">{% if fb.q5_satisfaction == 4 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q5_satisfaction == 3 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q5_satisfaction == 2 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q5_satisfaction == 1 %}✓{% endif %}</td>
            </tr>
            <tr>
                <td style="text-align: center;">6</td>
                <td>How do you estimate knowledge of our laboratory analyst?</td>
                <td style="text-align: center;">{% if fb.q6_knowledge == 4 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q6_knowledge == 3 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q6_knowledge == 2 %}✓{% endif %}</td>
                <td style="text-align: center;">{% if fb.q6_knowledge == 1 %}✓{% endif %}</td>
            </tr>
            <tr>
                <td colspan="2" style="font-weight: bold; text-align: right;">Total (For Lab use only)</td>
                <td colspan="4" style="text-align: center; font-weight: bold;">{{ fb.total_score }}</td>
            </tr>
            <tr>
                <td colspan="2" style="font-weight: bold; text-align: right;">Overall Rating (Total/24) %</td>
                <td colspan="4" style="text-align: center; font-weight: bold;">{{ fb.percentage }} %</td>
            </tr>
        </tbody>
    </table>
    
    <div style="border: 1px solid #000; padding: 10px; min-height: 80px; margin-bottom: 20px;">
        <strong>Any specific comments / complaint / suggestion or feedback you would like to add:</strong><br/>
        {{ fb.comments|default:""|linebreaksbr }}
    </div>
    
    <table class="noborder">
        <tr>
            <td style="width: 50%;"><strong>Customer’s Signature:</strong> _______________________</td>
            <td style="width: 50%;"><strong>Date:</strong> _______________________</td>
        </tr>
    </table>
    
    {% if not forloop.last %}<pdf:nextpage>{% endif %}
    {% endfor %}
    """
)
