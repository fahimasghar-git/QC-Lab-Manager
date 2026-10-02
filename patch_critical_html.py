import re
import os

def replace_in_file(path, replacements):
    if not os.path.exists(path): return
    with open(path, 'r') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, 'w') as f:
        f.write(content)

# 12.03 Certificate of Analysis
coa_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/certificate_of_analysis.html'
coa_old = """    <table class="noborder" style="margin-top: 50px;">
        <tr>
            <td style="width: 50%; text-align: center;">______________________<br/><br/><strong>Verified By</strong></td>
            <td style="width: 50%; text-align: center;">______________________<br/><br/><strong>Approved By</strong></td>
        </tr>
    </table>"""
coa_new = """    <table class="noborder" style="margin-top: 50px;">
        <tr>
            <td style="width: 50%; text-align: center;">
                {% if sample.verified_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ sample.verified_by.get_full_name }}<br/>
                    {{ sample.verified_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Verified By</strong>
            </td>
            <td style="width: 50%; text-align: center;">
                {% if sample.approved_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ sample.approved_by.get_full_name }}<br/>
                    {{ sample.approved_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Approved By</strong>
            </td>
        </tr>
    </table>"""
replace_in_file(coa_path, [(coa_old, coa_new)])

# 14.01 Non-Conformance
nc_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/templates/management/non_conformance_form.html'
nc_old = """    <table class="noborder" style="margin-top: 50px;">
        <tr>
            <td style="width: 33%; text-align: center;">______________________<br/><br/><strong>Initiated By</strong></td>
            <td style="width: 33%; text-align: center;">______________________<br/><br/><strong>Evaluated By (QCM)</strong></td>
            <td style="width: 33%; text-align: center;">______________________<br/><br/><strong>Approved By (CEO)</strong></td>
        </tr>
    </table>"""
nc_new = """    <table class="noborder" style="margin-top: 50px;">
        <tr>
            <td style="width: 33%; text-align: center;">
                {% if nc.prepared_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ nc.prepared_by.get_full_name }}<br/>
                    {{ nc.prepared_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Initiated By</strong>
            </td>
            <td style="width: 33%; text-align: center;">
                {% if nc.reviewed_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ nc.reviewed_by.get_full_name }}<br/>
                    {{ nc.reviewed_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Evaluated By (QCM)</strong>
            </td>
            <td style="width: 33%; text-align: center;">
                {% if nc.approved_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ nc.approved_by.get_full_name }}<br/>
                    {{ nc.approved_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Approved By (CEO)</strong>
            </td>
        </tr>
    </table>"""
replace_in_file(nc_path, [(nc_old, nc_new)])

# 4.02 Equipment Master List
eq_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/equipment_master_list.html'
eq_old = """    <table class="noborder" style="margin-top: 50px;">
        <tr>
            <td style="width: 33%; text-align: center;">______________________<br/><br/><strong>Prepared By</strong></td>
            <td style="width: 33%; text-align: center;">______________________<br/><br/><strong>Reviewed By</strong></td>
            <td style="width: 33%; text-align: center;">______________________<br/><br/><strong>Approved By</strong></td>
        </tr>
    </table>"""
eq_new = """    <table class="noborder" style="margin-top: 50px;">
        <tr>
            <td style="width: 33%; text-align: center;">
                {% if equipments.0.prepared_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ equipments.0.prepared_by.get_full_name }}<br/>
                    {{ equipments.0.prepared_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Prepared By</strong>
            </td>
            <td style="width: 33%; text-align: center;">
                {% if equipments.0.reviewed_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ equipments.0.reviewed_by.get_full_name }}<br/>
                    {{ equipments.0.reviewed_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Reviewed By</strong>
            </td>
            <td style="width: 33%; text-align: center;">
                {% if equipments.0.approved_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ equipments.0.approved_by.get_full_name }}<br/>
                    {{ equipments.0.approved_at|date:"d-m-Y H:i" }}
                {% else %}
                    ______________________
                {% endif %}
                <br/><br/><strong>Approved By</strong>
            </td>
        </tr>
    </table>"""
replace_in_file(eq_path, [(eq_old, eq_new)])

print("Patched critical HTML files.")

