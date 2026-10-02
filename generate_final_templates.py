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

# 19.01 Assignment
write_template(
    'samples/templates/samples/assignment_form.html',
    'Assignment, Summary and Review Form', '19.01', False,
    """
    {% for sample in samples %}
    <table class="noborder">
        <tr>
            <td style="width: 15%; font-weight: bold;">Product Name:</td>
            <td style="width: 35%; text-decoration: underline;">{{ sample.product_name }}</td>
            <td style="width: 15%; font-weight: bold;">Batch/Lot#:</td>
            <td style="width: 35%; text-decoration: underline;">{{ sample.batch_number|default:"-" }}</td>
        </tr>
        <tr>
            <td style="font-weight: bold;">Assigned Date:</td>
            <td style="text-decoration: underline;">{{ sample.assigned_date|date:"d-m-Y"|default:"-" }}</td>
            <td style="font-weight: bold;">Due Date:</td>
            <td style="text-decoration: underline;">{{ sample.due_date|date:"d-m-Y"|default:"-" }}</td>
        </tr>
        <tr>
            <td style="font-weight: bold;">Container type:</td>
            <td style="text-decoration: underline;">{{ sample.container_type|default:"-" }}</td>
            <td style="font-weight: bold;">QC#:</td>
            <td style="text-decoration: underline;">{{ sample.sample_id }}</td>
        </tr>
    </table>
    
    <table>
        <thead>
            <tr>
                <th>Sr. No.</th>
                <th>Assigned To</th>
                <th>Parameter</th>
                <th>Results (Units)</th>
                <th>Results Date</th>
                <th>Remarks</th>
            </tr>
        </thead>
        <tbody>
            {% for test in sample.test_results.all %}
            <tr>
                <td style="text-align: center;">{{ forloop.counter }}</td>
                <td style="text-align: center;">{{ test.assigned_to.get_full_name|default:"-" }}</td>
                <td style="text-align: center;">{{ test.parameter.name }}</td>
                <td style="text-align: center;">{{ test.result_value|default:"-" }}</td>
                <td style="text-align: center;">{{ test.verified_at|date:"d-m-Y"|default:"-" }}</td>
                <td>{{ test.remarks|default:"" }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="6" style="text-align: center; padding: 20px;">No tests assigned.</td></tr>
            {% endfor %}
        </tbody>
    </table>
    {% if not forloop.last %}<pdf:nextpage>{% endif %}
    {% endfor %}
    """
)

# 22.01 Sample Return
write_template(
    'samples/templates/samples/sample_return_form.html',
    'Sample Return Form', '22.01', False,
    """
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Sample ID</th>
                <th style="width: 25%;">Sample Return Date</th>
                <th style="width: 50%;">Reason for sample return</th>
            </tr>
        </thead>
        <tbody>
            {% for ret in returns %}
            <tr>
                <td style="text-align: center;">{{ ret.sample.sample_id }}</td>
                <td style="text-align: center;">{{ ret.return_date|date:"d-m-Y" }}</td>
                <td>{{ ret.reason }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    """
)

# 17.14 Lab Cleaning
write_template(
    'management/templates/management/lab_cleaning_inspection.html',
    'Lab Cleaning Inspection Sheet', '17.14', False,
    """
    {% for ins in inspections %}
    <table class="noborder">
        <tr>
            <td style="font-weight: bold; width: 15%;">Section/Area:</td>
            <td style="text-decoration: underline; width: 35%;">{{ ins.section_area }}</td>
            <td style="font-weight: bold; width: 15%;">Month:</td>
            <td style="text-decoration: underline; width: 35%;">{{ ins.month_year }}</td>
        </tr>
    </table>
    
    <table>
        <thead>
            <tr>
                <th rowspan="2" style="width: 10%;">Date</th>
                <th colspan="3">Daily Tasks</th>
                <th rowspan="2" style="width: 15%;">Checked By</th>
                <th rowspan="2" style="width: 15%;">Verified By</th>
            </tr>
            <tr>
                <th style="font-size: 9px;">Floor, Sanitary Sinks, Taps</th>
                <th style="font-size: 9px;">Bench Top / Shelves</th>
                <th style="font-size: 9px;">Equipment</th>
            </tr>
        </thead>
        <tbody>
            {% for daily in ins.daily_records.all %}
            <tr>
                <td style="text-align: center;">{{ daily.date|date:"d" }}</td>
                <td style="text-align: center;">{% if daily.floor_sinks_taps %}Yes{% else %}No{% endif %}</td>
                <td style="text-align: center;">{% if daily.bench_top_shelves %}Yes{% else %}No{% endif %}</td>
                <td style="text-align: center;">{% if daily.equipment %}Yes{% else %}No{% endif %}</td>
                <td style="text-align: center;">{{ daily.checked_by|default:"" }}</td>
                <td style="text-align: center;">{{ daily.verified_by|default:"" }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="6" style="text-align: center;">No daily records created yet.</td></tr>
            {% endfor %}
        </tbody>
    </table>
    
    <table style="margin-top: 20px;">
        <tr><td class="section-header" colspan="2" style="background-color: #d9d9d9; font-weight: bold;">Weekly & Monthly Tasks</td></tr>
        <tr>
            <td style="width: 80%;">Cleaning Of Lights and AC's (Monthly)</td>
            <td style="width: 20%; text-align: center;">{% if ins.lights_acs_cleaned %}Done{% else %}Pending{% endif %}</td>
        </tr>
        <tr>
            <td>Overall Cleaning and Spray in Lab (Monthly)</td>
            <td style="text-align: center;">{% if ins.overall_spray %}Done{% else %}Pending{% endif %}</td>
        </tr>
        <tr>
            <td>Cleaning of Racks, Cabinets and Fumehood (Weekly)</td>
            <td style="text-align: center;">{% if ins.racks_cabinets %}Done{% else %}Pending{% endif %}</td>
        </tr>
    </table>
    
    {% if not forloop.last %}<pdf:nextpage>{% endif %}
    {% endfor %}
    """
)

