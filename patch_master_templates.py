import re

def patch_template(path):
    with open(path, 'r') as f:
        content = f.read()

    # The HTML string for the signature block
    old_sig = """    <table class="noborder" style="margin-top: 50px;">
        <tr>
            <td style="width: 33%; text-align: center;">______________________<br/><br/>Prepared By</td>
            <td style="width: 33%; text-align: center;">______________________<br/><br/>Reviewed By</td>
            <td style="width: 33%; text-align: center;">______________________<br/><br/>Approved By</td>
        </tr>
    </table>"""
    
    new_sig = """    <table class="noborder" style="margin-top: 50px;">
        <tr>
            <td style="width: 33%; text-align: center;">
                {% if records.0.prepared_at or files.0.prepared_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ records.0.prepared_by.get_full_name|default:files.0.prepared_by.get_full_name }}<br/>
                    {{ records.0.prepared_at|date:"d-m-Y H:i"|default:files.0.prepared_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Prepared By</strong>
            </td>
            <td style="width: 33%; text-align: center;">
                {% if records.0.reviewed_at or files.0.reviewed_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ records.0.reviewed_by.get_full_name|default:files.0.reviewed_by.get_full_name }}<br/>
                    {{ records.0.reviewed_at|date:"d-m-Y H:i"|default:files.0.reviewed_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Reviewed By</strong>
            </td>
            <td style="width: 33%; text-align: center;">
                {% if records.0.approved_at or files.0.approved_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ records.0.approved_by.get_full_name|default:files.0.approved_by.get_full_name }}<br/>
                    {{ records.0.approved_at|date:"d-m-Y H:i"|default:files.0.approved_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Approved By</strong>
            </td>
        </tr>
    </table>"""

    content = content.replace(old_sig, new_sig)
    with open(path, 'w') as f:
        f.write(content)

patch_template('/Users/fahimasghar/Documents/QC-Lab-Manager/management/templates/management/master_list_records.html')
patch_template('/Users/fahimasghar/Documents/QC-Lab-Manager/management/templates/management/master_list_files.html')
print("Patched HTML templates for signatures")
