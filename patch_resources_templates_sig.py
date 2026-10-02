import re

def patch_template(path, old_sig, new_sig):
    with open(path, 'r') as f:
        content = f.read()
    if old_sig in content:
        content = content.replace(old_sig, new_sig)
        with open(path, 'w') as f:
            f.write(content)
        print(f"Patched {path}")
    else:
        print(f"Could not find old_sig in {path}")

# 6.05 Comparative Statement
old_605 = """    <table style="border: none; margin-top: 50px;">
        <tr>
            <td style="border: none; width: 50%; text-align: center;">
                _____________________________________<br/><br/>
                {{ cs.prepared_by.get_full_name|default:"Prepared By" }}
            </td>
            <td style="border: none; width: 50%; text-align: center;">
                _____________________________________<br/><br/>
                {{ cs.approved_by.get_full_name|default:"Approved By" }}
            </td>
        </tr>
    </table>"""
new_605 = """    <table style="border: none; margin-top: 50px;">
        <tr>
            <td style="border: none; width: 50%; text-align: center;">
                {% if cs.prepared_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ cs.prepared_by.get_full_name }}<br/>
                    {{ cs.prepared_at|date:"d-m-Y H:i" }}
                {% else %}
                    _____________________________________<br/><br/>
                    {{ cs.prepared_by.get_full_name|default:"Prepared By" }}
                {% endif %}
            </td>
            <td style="border: none; width: 50%; text-align: center;">
                {% if cs.approved_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ cs.approved_by.get_full_name }}<br/>
                    {{ cs.approved_at|date:"d-m-Y H:i" }}
                {% else %}
                    _____________________________________<br/><br/>
                    {{ cs.approved_by.get_full_name|default:"Approved By" }}
                {% endif %}
            </td>
        </tr>
    </table>"""
patch_template('/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/comparative_statement.html', old_605, new_605)

# 6.06 Supplier Evaluation Plan
old_606 = """    <table style="border: none; margin-top: 50px;">
        <tr>
            <td style="border: none; width: 50%; text-align: center;">
                _____________________________________<br/><br/>
                {{ plan.prepared_by.get_full_name|default:"Prepared By" }}<br/>
                <strong>Date:</strong> {{ plan.prepared_date|date:"d-m-Y"|default:"____________________" }}
            </td>
            <td style="border: none; width: 50%; text-align: center;">
                _____________________________________<br/><br/>
                {{ plan.approved_by.get_full_name|default:"Approved by (QCM)" }}<br/>
                <strong>Date:</strong> {{ plan.approved_date|date:"d-m-Y"|default:"____________________" }}
            </td>
        </tr>
    </table>"""
new_606 = """    <table style="border: none; margin-top: 50px;">
        <tr>
            <td style="border: none; width: 50%; text-align: center;">
                {% if plan.prepared_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ plan.prepared_by.get_full_name }}<br/>
                    {{ plan.prepared_at|date:"d-m-Y H:i" }}<br/>
                    <strong>Prepared By</strong>
                {% else %}
                    _____________________________________<br/><br/>
                    {{ plan.prepared_by.get_full_name|default:"Prepared By" }}<br/>
                    <strong>Date:</strong> ____________________
                {% endif %}
            </td>
            <td style="border: none; width: 50%; text-align: center;">
                {% if plan.approved_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ plan.approved_by.get_full_name }}<br/>
                    {{ plan.approved_at|date:"d-m-Y H:i" }}<br/>
                    <strong>Approved by (QCM)</strong>
                {% else %}
                    _____________________________________<br/><br/>
                    {{ plan.approved_by.get_full_name|default:"Approved by (QCM)" }}<br/>
                    <strong>Date:</strong> ____________________
                {% endif %}
            </td>
        </tr>
    </table>"""
patch_template('/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/supplier_evaluation_plan.html', old_606, new_606)

